from ctrader_open_api import Client, EndPoints
from ctrader_open_api.protobuf import Protobuf
from ctrader_open_api.tcpProtocol import TcpProtocol

def on_connected(client):
    print("CONNECTED")

def on_disconnected(client, reason):
    print("DISCONNECTED:", reason)

if __name__ == "__main__":
    print("STARTING CLIENT...")

    protocol = TcpProtocol()   # ✅ БЕЗ аргументов

    client = Client(
        EndPoints.PROTOBUF_DEMO_HOST,
        EndPoints.PROTOBUF_PORT,
        protocol
    )

    client.setConnectedCallback(on_connected)
    client.setDisconnectedCallback(on_disconnected)

    print("CLIENT CREATED")

    client.startService()

    print("SERVICE STARTED")