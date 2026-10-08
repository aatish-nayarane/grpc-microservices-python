from fastapi import FastAPI
import asyncio
from app.core import  grpc_client 

app = FastAPI()

@app.post("/compute/create")
async def create_compute(vm_id: str):
    net = await grpc_client.call_network_service(vm_id)

    return {
        "vm_id": vm_id,
        "allocated_ip": net.ip_address,
        "network_success": net.success
    }
