PROTO_DIR = proto
GO_OUT = backend/api
PY_OUT = frontend/api
PROTO_FILE = $(PROTO_DIR)/claritas.proto

.PHONY: all go python clean dirs deps

all: dirs go python

dirs:
	# Create target directories if they do not exist
	mkdir -p $(GO_OUT)
	mkdir -p $(PY_OUT)

go:
	# Generate Go protobuf and gRPC code
	protoc -I=$(PROTO_DIR) \
		--go_out=$(GO_OUT) --go_opt=paths=source_relative \
		--go-grpc_out=$(GO_OUT) --go-grpc_opt=paths=source_relative \
		$(PROTO_FILE)

python:
	# Generate Python protobuf and gRPC code
	python -m grpc_tools.protoc -I=$(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		$(PROTO_FILE)
	sed -i 's/^import claritas_pb2 as claritas__pb2/from . import claritas_pb2 as claritas__pb2/' $(PY_OUT)/claritas_pb2_grpc.py
	touch $(PY_OUT)/__init__.py

clean:
	# Remove all generated files
	rm -rf $(GO_OUT)/*
	rm -rf $(PY_OUT)/*

deps:
	# Install necessary plugins for Go
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
