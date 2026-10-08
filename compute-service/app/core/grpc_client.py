import grpc
from grpc import aio
from app.grpc import network_pb2
from app.grpc import network_pb2_grpc

async def call_network_service(vm_id: str):
    async with aio.insecure_channel("network-service:50052") as channel:
        stub = network_pb2_grpc.NetworkServiceStub(channel)

        response = await stub.AllocateIP(
            network_pb2.AllocateIPRequest(vm_id=vm_id)
        )

        return response
