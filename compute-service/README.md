# gRPC Internal Service Communication

A Python-based microservices project demonstrating **internal service-to-service communication using gRPC**.

The project contains separate Compute and Network services that communicate internally using **gRPC and Protocol Buffers (Protobuf)**.

The goal is to understand how gRPC can be used for fast, strongly typed communication between internal microservices.

## Architecture

```text
                    Client / External API
                            |
                            v
                  +-------------------+
                  |   Compute Service |
                  +---------+---------+
                            |
                     gRPC Client
                            |
                            | Internal gRPC
                            v
                  +-------------------+
                  |   Network Service |
                  +-------------------+
```

The Compute Service acts as a gRPC client and communicates with the Network Service using the generated Protobuf interface.

## Project Structure

```text
.
├── compute-service
│   ├── app
│   │   ├── api
│   │   │   └── v1
│   │   │       └── compute_controller.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── grpc_client.py
│   │   ├── grpc
│   │   │   ├── network_pb2_grpc.py
│   │   │   ├── network_pb2.py
│   │   │   └── network.proto
│   │   ├── main.py
│   │   └── utils
│   │       └── logger.py
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
│
└── network-service
    ├── app
    │   ├── api
    │   │   └── v1
    │   │       └── network_controller.py
    │   ├── core
    │   │   ├── config.py
    │   │   └── service_logic.py
    │   ├── grpc
    │   │   ├── network_pb2_grpc.py
    │   │   ├── network_pb2.py
    │   │   └── network.proto
    │   ├── main.py
    │   └── utils
    │       └── logger.py
    ├── Dockerfile
    ├── README.md
    └── requirements.txt
```

## Services

### Compute Service

The Compute Service exposes the application-facing API and acts as a **gRPC client** for the Network Service.

Important components:

```text
compute-service/app/
├── api/
│   └── v1/
│       └── compute_controller.py
├── core/
│   ├── config.py
│   └── grpc_client.py
├── grpc/
│   ├── network.proto
│   ├── network_pb2.py
│   └── network_pb2_grpc.py
├── main.py
└── utils/
    └── logger.py
```

`grpc_client.py` contains the internal gRPC client implementation used to communicate with the Network Service.

### Network Service

The Network Service acts as the **gRPC server** and handles requests received from the Compute Service.

Important components:

```text
network-service/app/
├── api/
│   └── v1/
│       └── network_controller.py
├── core/
│   ├── config.py
│   └── service_logic.py
├── grpc/
│   ├── network.proto
│   ├── network_pb2.py
│   └── network_pb2_grpc.py
├── main.py
└── utils/
    └── logger.py
```

`service_logic.py` contains the internal business logic executed by the Network Service.

## gRPC Communication Flow

The communication flow is:

```text
Request
   |
   v
Compute Controller
   |
   v
gRPC Client
   |
   | Protobuf Request
   v
Network Service
   |
   v
Network Controller
   |
   v
Service Logic
   |
   v
Protobuf Response
   |
   v
gRPC Client
   |
   v
Compute Service
```

## Protocol Buffers

The service contract is defined using:

```text
network.proto
```

The `.proto` file defines:

- Services
- RPC methods
- Request messages
- Response messages
- Field types

Example structure:

```proto
service NetworkService {
    rpc SomeOperation(SomeRequest) returns (SomeResponse);
}
```

The Python gRPC code is generated from the `.proto` definition.

Generated files include:

```text
network_pb2.py
network_pb2_grpc.py
```

### `network_pb2.py`

Contains the generated Protocol Buffer message classes.

### `network_pb2_grpc.py`

Contains the generated gRPC client and server classes.

These generated files should normally be regenerated whenever the `.proto` contract changes.

## gRPC Client

The Compute Service uses a gRPC client to communicate with the Network Service.

Conceptually:

```text
Compute Service
      |
      v
Create Channel
      |
      v
Create Stub
      |
      v
Call RPC
      |
      v
Network Service
```

The client typically creates a channel such as:

```python
channel = grpc.insecure_channel("network-service:50051")
```

and then creates a generated stub:

```python
stub = NetworkServiceStub(channel)
```

The RPC can then be called through the stub.

## gRPC Server

The Network Service starts a gRPC server and registers the generated service implementation.

Conceptually:

```text
Network Service
      |
      v
Create gRPC Server
      |
      v
Register Service
      |
      v
Bind Port
      |
      v
Start Server
```

The server listens for internal gRPC requests from other services.

## Why gRPC?

gRPC is useful for internal microservice communication because it provides:

- Strongly typed contracts
- Protocol Buffer serialization
- HTTP/2 transport
- Efficient binary communication
- Generated client/server code
- Streaming support
- Deadlines and timeouts
- Metadata support
- Service definitions through `.proto`

## REST vs gRPC

| Feature | REST | gRPC |
|---|---|---|
| Data format | Usually JSON | Protobuf |
| Transport | HTTP/1.1 commonly | HTTP/2 |
| Contract | OpenAPI commonly | `.proto` |
| Serialization | Text-based | Binary |
| Code generation | Optional | Built-in |
| Streaming | Limited/custom | Native support |
| Internal microservices | Common | Very suitable |

## Internal Communication

This project focuses specifically on **internal service communication**.

Instead of:

```text
Compute Service
      |
      v
HTTP REST
      |
      v
Network Service
```

the services communicate using:

```text
Compute Service
      |
      | gRPC
      v
Network Service
```

This approach is useful when multiple internal services need strongly typed and efficient communication.

## Configuration

Service configuration is maintained separately in:

```text
app/core/config.py
```

Typical configuration values include:

```text
GRPC_HOST
GRPC_PORT
NETWORK_SERVICE_HOST
NETWORK_SERVICE_PORT
```

For production deployments, sensitive configuration should be supplied using environment variables or a secrets-management system.

## Running the Services

Create separate Python environments or install the dependencies defined in each service.

### Compute Service

```bash
cd compute-service

pip install -r requirements.txt

python -m app.main
```

### Network Service

```bash
cd network-service

pip install -r requirements.txt

python -m app.main
```

The Network Service should be running before the Compute Service attempts to make internal gRPC requests.

## Docker

Both services contain their own Dockerfile.

Build the Compute Service:

```bash
docker build -t compute-service ./compute-service
```

Build the Network Service:

```bash
docker build -t network-service ./network-service
```

Run the services on the same Docker network:

```bash
docker network create internal-network
```

Run Network Service:

```bash
docker run --network internal-network \
    --name network-service \
    network-service
```

Run Compute Service:

```bash
docker run --network internal-network \
    --name compute-service \
    compute-service
```

The Compute Service can then communicate with the Network Service using the Docker service/container name instead of `localhost`.

## Error Handling

Internal gRPC communication should handle failures such as:

- Connection refused
- Service unavailable
- Request timeout
- Deadline exceeded
- Invalid arguments
- Internal server errors
- Network failures

gRPC status codes can be used to distinguish different failure conditions.

## Timeouts and Deadlines

Internal service calls should use deadlines/timeouts to avoid indefinitely waiting for another service.

Conceptually:

```text
Compute Service
      |
      | Request
      |-------> Network Service
      |
      | Timeout / Deadline
      |
      X
```

This is particularly important in distributed systems where one unavailable service should not block another service indefinitely.

## Logging

Each service contains a logging utility:

```text
app/utils/logger.py
```

Logging can be used to track:

- Incoming requests
- Outgoing gRPC calls
- RPC failures
- Response times
- Service errors
- Debug information

## Testing

Run tests from the appropriate service directory:

```bash
python -m pytest
```

For more verbose output:

```bash
python -m pytest -v
```

Integration tests can verify communication between the Compute and Network services.

## Key Concepts Demonstrated

This project demonstrates:

- gRPC
- Protocol Buffers
- Service-to-service communication
- gRPC client
- gRPC server
- Generated Protobuf code
- RPC methods
- HTTP/2
- Internal APIs
- Microservice architecture
- Deadlines and timeouts
- Error handling
- Docker networking
- Service discovery
- Logging
- Integration testing

## Learning Goals

The main goal of this project is to understand how **gRPC can be used for internal communication between microservices**.

Key areas include:

1. Designing `.proto` service contracts
2. Generating Python gRPC code
3. Implementing gRPC servers
4. Implementing gRPC clients
5. Calling internal RPC methods
6. Handling gRPC errors
7. Using deadlines and timeouts
8. Running services independently
9. Connecting services through Docker networking
10. Structuring production-style Python microservices

## Future Improvements

Possible improvements include:

- Add authentication between services
- Add TLS/mTLS
- Add gRPC interceptors
- Add retry policies
- Add circuit breaker integration
- Add distributed tracing
- Add Prometheus metrics
- Add health-check service
- Add service discovery
- Add Docker Compose
- Add Kubernetes deployment
- Add asynchronous gRPC support

## License

This project is licensed under the terms specified in the `LICENSE` file.