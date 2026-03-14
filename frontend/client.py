import grpc
from PySide6.QtCore import QThread, Signal
from api import claritas_pb2
from api import claritas_pb2_grpc

class GrpcDataStreamer(QThread):
    chunk_received = Signal(list, list)
    finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, file_path, x_col, y_col):
        super().__init__()
        self.file_path = file_path
        self.x_col = x_col
        self.y_col = y_col

    def run(self):
        channel = grpc.insecure_channel('unix:///tmp/claritas.sock')
        stub = claritas_pb2_grpc.ClaritasEngineStub(channel)

        request = claritas_pb2.ParseRequest(
            file_path=self.file_path,
            x_column=self.x_col,
            y_column=self.y_col,
            chunk_size=5000
        )

        try:
            response_stream = stub.StreamData(request)
            
            for chunk in response_stream:
                if chunk.error_message:
                    self.error_occurred.emit(chunk.error_message)
                    break
            if chunk.x_is_string:
                x_data = list(chunk.x_string_values)
            else:
                x_data = list(chunk.x_num_values)

            if chunk.y_is_string:
                y_data = list(chunk.y_string_values)
            else:
                y_data = list(chunk.y_num_values)

            self.chunk_received.emit(x_data, y_data)
                
        except grpc.RpcError as e:
            self.error_occurred.emit(f"gRPC Error: {e.details()}")
        finally:
            channel.close()
            self.finished.emit()
