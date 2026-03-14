package main

import (
	"context"
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"slices"
	"strconv"
	"syscall"

	"google.golang.org/grpc"

	pb "github.com/berezovskyivalerii/Claritas/backend/api"
)

const sockAddr = "/tmp/claritas.sock"

type server struct {
	pb.UnimplementedClaritasEngineServer
}

// Ping implements the health check method
func (s *server) Ping(ctx context.Context, in *pb.Empty) (*pb.HealthStatus, error) {
	log.Println("Received Ping request from Python client")
	return &pb.HealthStatus{Status: "OK"}, nil
}

// GetHeaders returns headers from the file
func (s *server) GetHeaders(ctx context.Context, in *pb.FileRequest) (*pb.HeadersResponse, error) {
	log.Printf("Received request to get headers for file: %s\n", in.GetFilePath())

	file, err := os.Open(in.GetFilePath())
	if err != nil {
		fmt.Println("Error: ", err)
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	headers, err := reader.Read()
	if err != nil {
		fmt.Println("Error: ", err)
	}

	return &pb.HeadersResponse{
		Columns: headers,
	}, nil
}

// RawBatch represents a chunk of unparsed string rows
type RawBatch struct {
	Records [][]string
}

func (s *server) StreamData(in *pb.ParseRequest, stream pb.ClaritasEngine_StreamDataServer) error {
	log.Printf("Received stream request for file: %s\n", in.GetFilePath())

	file, err := os.Open(in.GetFilePath())
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1

	headers, err := reader.Read()
	if err != nil && err != io.EOF {
		return fmt.Errorf("failed to read headers: %w", err)
	}

	xIndex := slices.Index(headers, in.GetXColumn())
	yIndex := slices.Index(headers, in.GetYColumn())
	if xIndex == -1 || yIndex == -1 {
		return fmt.Errorf("requested headers were not found")
	}

	xIsStr := false
	yIsStr := false

	// Peek at the first row to determine data types
	peekRow, err := reader.Read()
	if err == nil {
		if _, parseErr := strconv.ParseFloat(peekRow[xIndex], 64); parseErr != nil {
			xIsStr = true
		}
		if _, parseErr := strconv.ParseFloat(peekRow[yIndex], 64); parseErr != nil {
			yIsStr = true
		}
		
		file.Seek(0, 0)
		reader = csv.NewReader(file)
		reader.Read() // skip headers again
	}

	// 1. Adaptive Window Calculation
	fileStat, err := file.Stat()
	if err != nil {
		return fmt.Errorf("failed to get file stats: %w", err)
	}

	estimatedRows := fileStat.Size() / 30
	windowSize := int(estimatedRows / 2000)
	
	// Disable decimation completely for small files OR if any column is a string
	if windowSize < 1 || xIsStr || yIsStr {
		windowSize = 1 
	}
	
	log.Printf("File size: %d bytes. Estimated rows: %d. Calculated window size: %d\n", fileStat.Size(), estimatedRows, windowSize)

	chunkCapacity := 10000 
	xNumChunk := make([]float64, 0, chunkCapacity)
	yNumChunk := make([]float64, 0, chunkCapacity)
	xStrChunk := make([]string, 0, chunkCapacity)
	yStrChunk := make([]string, 0, chunkCapacity)

	var eofReached bool

	// 2. Main Processing Loop
	for !eofReached {
		var minVal, maxVal float64
		var minX, maxX float64
		isFirstInWindow := true
		validPointsInWindow := 0

		for i := 0; i < windowSize; i++ {
			record, err := reader.Read()
			if err == io.EOF {
				eofReached = true
				break
			}
			if err != nil || len(record) <= xIndex || len(record) <= yIndex {
				continue 
			}

			var xNum, yNum float64
			var errX, errY error

			// Parse only if the column is numeric
			if !xIsStr {
				xNum, errX = strconv.ParseFloat(record[xIndex], 64)
			}
			if !yIsStr {
				yNum, errY = strconv.ParseFloat(record[yIndex], 64)
			}

			if errX == nil && errY == nil {
				if windowSize == 1 {
					// Direct append for strings or small files
					if xIsStr {
						xStrChunk = append(xStrChunk, record[xIndex])
					} else {
						xNumChunk = append(xNumChunk, xNum)
					}
					
					if yIsStr {
						yStrChunk = append(yStrChunk, record[yIndex])
					} else {
						yNumChunk = append(yNumChunk, yNum)
					}
				} else {
					// Min-Max Decimation for numeric data
					if isFirstInWindow {
						minVal = yNum
						maxVal = yNum
						minX = xNum
						maxX = xNum
						isFirstInWindow = false
					} else {
						if yNum < minVal {
							minVal = yNum
							minX = xNum
						}
						if yNum > maxVal {
							maxVal = yNum
							maxX = xNum
						}
					}
				}
				validPointsInWindow++
			}
		}

		// Append decimated points after the window loop finishes
		if windowSize > 1 && validPointsInWindow > 0 {
			if minX < maxX {
				xNumChunk = append(xNumChunk, minX, maxX)
				yNumChunk = append(yNumChunk, minVal, maxVal)
			} else if minX > maxX {
				xNumChunk = append(xNumChunk, maxX, minX)
				yNumChunk = append(yNumChunk, maxVal, minVal)
			} else {
				xNumChunk = append(xNumChunk, minX)
				yNumChunk = append(yNumChunk, minVal)
			}
		}

		// Check current length to decide if we need to send the chunk
		currentLen := len(xNumChunk)
		if xIsStr {
			currentLen = len(xStrChunk)
		}

		// 3. Send chunk if capacity reached or file ended
		if currentLen >= chunkCapacity-2 || eofReached {
			if currentLen > 0 {
				sendErr := stream.Send(&pb.DataChunk{
					XNumValues: xNumChunk,
					YNumValues: yNumChunk,
					XStringValues: xStrChunk,
					YStringValues: yStrChunk,
					XIsString:  xIsStr,
					YIsString:  yIsStr,
				})
				
				if sendErr != nil {
					return fmt.Errorf("stream send error: %w", sendErr)
				}
				
				// Reset slices but keep capacity
				xNumChunk = xNumChunk[:0]
				yNumChunk = yNumChunk[:0]
				xStrChunk = xStrChunk[:0]
				yStrChunk = yStrChunk[:0]
			}
		}
	}

	return nil
}

func main() {
	// Clean up the socket file if it exists from a previous crash
	if err := os.RemoveAll(sockAddr); err != nil {
		log.Fatalf("Failed to remove existing socket file: %v", err)
	}

	// Create a listener on the Unix socket
	lis, err := net.Listen("unix", sockAddr)
	if err != nil {
		log.Fatalf("Failed to listen on socket: %v", err)
	}
	defer os.RemoveAll(sockAddr)

	// Create a new gRPC server instance
	grpcServer := grpc.NewServer()

	// Register our service implementation with the gRPC server
	pb.RegisterClaritasEngineServer(grpcServer, &server{})

	// Create a channel to receive OS signals for graceful shutdown
	stopChan := make(chan os.Signal, 1)
	signal.Notify(stopChan, os.Interrupt, syscall.SIGTERM)

	// Start the server in a separate goroutine
	go func() {
		log.Printf("gRPC server listening on unix://%s\n", sockAddr)
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("Failed to serve: %v", err)
		}
	}()

	<-stopChan
	log.Println("Shutting down gRPC server gracefully...")
	
	grpcServer.GracefulStop()
	log.Println("Server stopped")
}
