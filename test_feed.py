from ctrader_open_api import Client, EndPoints, TcpProtocol
from twisted.internet import reactor


class CTraderFeed:
    def __init__(self):

        self.client = Client(
            EndPoints.PROTOBUF_DEMO_HOST,
            EndPoints.PROTOBUF_PORT,
            TcpProtocol  # ✅ CLASS, НЕ instance
        )

        self.client.setConnectedCallback(self.on_connected)
        self.client.setDisconnectedCallback(self.on_disconnected)

        print("CLIENT CREATED")

    def connect(self):
        print("CONNECTING...")
        self.client.startService()
        print("SERVICE STARTED")

    def on_connected(self, client):
        print("CONNECTED TO CTRADER")

    def on_disconnected(self, client, reason):
        print("DISCONNECTED:", reason)


if __name__ == "__main__":
    feed = CTraderFeed()

    feed.connect()

    reactor.run()