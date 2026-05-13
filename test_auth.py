from ctrader_open_api import Client, EndPoints, Auth
from app.config.ctrader_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

client = Client(EndPoints.PROTOBUF_DEMO_HOST, EndPoints.PROTOBUF_PORT)

auth = Auth(client, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

print("AUTH INIT OK")