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

	// 1. Adaptive Window Calculation
	fileStat, err := file.Stat()
	if err != nil {
		return fmt.Errorf("failed to get file stats: %w", err)
	}

	// Estimate the number of rows (assuming ~30 bytes per row for a typical CSV with 2 floats)
	estimatedRows := fileStat.Size() / 30

	// We want to send approximately 4000 points (2000 windows) to keep UI responsive
	windowSize := int(estimatedRows / 2000)
	
	// Disable decimation completely for small files
	if windowSize < 1 {
		windowSize = 1 
	}
	
	log.Printf("File size: %d bytes. Estimated rows: %d. Calculated window size: %d\n", fileStat.Size(), estimatedRows, windowSize)

	chunkCapacity := 10000 
	xChunk := make([]float64, 0, chunkCapacity)
	yChunk := make([]float64, 0, chunkCapacity)

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

			xVal, errX := strconv.ParseFloat(record[xIndex], 64)
			yVal, errY := strconv.ParseFloat(record[yIndex], 64)

			if errX == nil && errY == nil {
				if isFirstInWindow {
					minVal = yVal
					maxVal = yVal
					minX = xVal
					maxX = xVal
					isFirstInWindow = false
				} else {
					if yVal < minVal {
						minVal = yVal
						minX = xVal
					}
					if yVal > maxVal {
						maxVal = yVal
						maxX = xVal
					}
				}
				validPointsInWindow++
			}
		}

		if validPointsInWindow > 0 {
			if minX < maxX {
				xChunk = append(xChunk, minX, maxX)
				yChunk = append(yChunk, minVal, maxVal)
			} else if minX > maxX {
				xChunk = append(xChunk, maxX, minX)
				yChunk = append(yChunk, maxVal, minVal)
			} else {
				// Perfect for windowSize == 1, appends only the exact point
				xChunk = append(xChunk, minX)
				yChunk = append(yChunk, minVal)
			}
		}

		// 3. Send chunk if capacity reached or file ended
		if len(xChunk) >= chunkCapacity-2 || eofReached {
			if len(xChunk) > 0 {
				sendErr := stream.Send(&pb.DataChunk{
					XValues: xChunk,
					YValues: yChunk,
				})
				if sendErr != nil {
					return fmt.Errorf("stream send error: %w", sendErr)
				}
				
				// Reset slice length but keep capacity
				xChunk = xChunk[:0]
				yChunk = yChunk[:0]
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
