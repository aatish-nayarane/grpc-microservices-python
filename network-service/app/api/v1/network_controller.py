import grpc
from grpc import aio
from app.grpc import network_pb2
from app.grpc import  network_pb2_grpc

class NetworkService(network_pb2_grpc.NetworkServiceServicer):

    async def AllocateIP(self, request, context):
        vm_id = request.vm_id
        print("Allocating IP for VM:", vm_id)

        # logic here…
        return network_pb2.AllocateIPResponse(
            ip_address="10.210.10.51",
            success=True
        )

async def serve():
    server = aio.server()
    network_pb2_grpc.add_NetworkServiceServicer_to_server(NetworkService(), server)

    server.add_insecure_port("[::]:50052")
    await server.start()
    print("Network Service Running on port 50052")
    await server.wait_for_termination()

if __name__ == "__main__":
    import asyncio
    asyncio.run(serve())
