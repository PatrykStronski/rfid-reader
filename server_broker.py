import time
import json
import paho.mqtt.client as mqtt
import db_management as dbm

QUEUE_ADDRESS="localhost"
QUEUE_TOPIC="logging"
client = mqtt.Client()
client.connect(QUEUE_ADDRESS)


def consume_message(client, user_data, msg):
    print("Consuming message")
    msg.payload = msg.payload.decode("utf-8")
    message = json.loads(msg.payload)
    print(message["status"])
    if (message["status"] == "health"):
        if (message["on"]):
            print("Instance "+message["instance_id"]+" started")
        else:
            print("Instance "+message["instance_id"]+" down")
    elif (message["status"] == "log"):
        print("Log from "+message["instance_id"]+" received")
        dbm.write_message(message["uid"], message["time"], message["instance_id"])

client.on_message = consume_message
print("Started broker server")
while 1:
    client.loop_start()
    client.subscribe(QUEUE_TOPIC, 2)
    time.sleep(1)
