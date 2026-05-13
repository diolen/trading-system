# app/data/ctrader_feed.py

from ctrader_open_api import Client, EndPoints
from ctrader_open_api.messages import OpenApiMessages_pb2 as messages
from ctrader_open_api import TcpProtocol
from ctrader_open_api.Protobuf import Protobuf

class CTraderFeed:

    def __init__(self, host, port, protocol):
        self.client = Client(host, port, protocol)

        self.client.setConnectedCallback(self.on_connected)
        self.client.setDisconnectedCallback(self.on_disconnected)

        self.client.setMessageReceivedCallback(self.on_message)

    def connect(self):
        print("Connecting to cTrader...")
        self.client.startService()

    # --- callbacks ---

    def on_connected(self, client):
        print("CONNECTED")

        # тут позже auth + subscribe
        self.request_candles()

    def on_disconnected(self, client, reason):
        print("DISCONNECTED:", reason)

    def on_message(self, client, message):
        # сюда будут приходить protobuf сообщения
        print("MESSAGE:", message)

    # --- data request ---

    def request_candles(self):
        print("Requesting candles...")

        # TODO: заменить на реальный proto request
        # (в зависимости от cTrader API version)

        request = messages.ProtoOAGetTrendbarsReq()
        request.symbolId = 1  # временно
        request.period = 5    # M5/M15 зависит от enum
        request.count = 100

        self.client.send(request)