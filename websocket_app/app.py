import time
import os
import websocket
from datetime import datetime
import json
from google.cloud import pubsub_v1

# set environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/key-gcloud.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "cryptos-gcp"

# finnub api key
with open('keys/finnhub_api_key.txt') as f:
    api_key = f.read()
    f.close()  


publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='allo_topic',
)
publisher.create_topic(name=topic_name)

def on_message(ws, message):
    json_message = json.loads(message)
    trades = json_message['data']

    for trade in trades:
        kafka_data = {}
        kafka_data["symbol"] = trade['s']
        kafka_data["price"] = trade['p']
        kafka_data["volume"] = trade['v']
        kafka_data["timestamp_unix"] = trade['t']
        kafka_data["conditions"] = trade['c']

        publisher.publish(topic_name, json.dumps(kafka_data).encode('utf-8'))
        
def on_error(ws, error):
    print(error)

# def on_close(ws):
#     print("### closed ###")

def on_close(ws):
    print(f"### closed ###")
    #restart the websocket connection
    # time.sleep(1)
    # print("### restart ###")
    # start_streaming()

    
def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


def start_streaming():
    websocket.enableTrace(True)
    # websocket.enableTrace(True, level="ERROR")
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + api_key ,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    start_streaming()