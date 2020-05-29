import time
import json
import tkinter
import paho.mqtt.client as mqtt
import db_management as dbm
import constants as consts

client=mqtt.Client()
client.tls_set("./config/ca.crt")
client.username_pw_set(username="server", password="server")
client.connect(consts.QUEUE_ADDRESS, consts.PORT)

def consume_message(client, user_data, msg):
    msg.payload = msg.payload.decode("utf-8")
    message = json.loads(msg.payload)
    if (message["status"] == "health"):
        if (message["on"]):
            print("Instance "+message["instance_id"]+" started")
        else:
            print("Instance "+message["instance_id"]+" down")
    elif (message["status"] == "log"):
        print("Log from "+message["instance_id"]+" received")
        dbm.write_message(message["uid"], message["time"], message["instance_id"])
        ack_msg = {"status": "received", "message": message}
        client.publish(consts.QUEUE_TOPIC_ACK + "/" + message["instance_id"], json.dumps(ack_msg))


client.on_message = consume_message
print("Started broker server")


while 1:
    client.loop_start()
    client.subscribe(consts.QUEUE_TOPIC, 2)
    time.sleep(1)
