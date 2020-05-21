import time
import json
import uuid
import paho.mqtt.client as mqtt

QUEUE_ADDRESS="localhost"
QUEUE_TOPIC="logging"
BROKER = "employee-verification" #using FQDN provided
PORT = 8883

client = mqtt.Client()
client.tls_set("../config/ca.crt")
client.connect(BROKER, PORT)
terminal_id = str(uuid.uuid4())

def save_uid_log(uid,time_read):
    s = "-"
    time_read=int(time_read)
    msg = {"status": "log", "time": time_read, "uid": s.join(uid), "instance_id": terminal_id}
    print("Sending message to server")
    client.publish(QUEUE_TOPIC, json.dumps(msg))

def initialize_reader():
    msg = {"status": "health", "on": 1, "instance_id": terminal_id}
    client.publish(QUEUE_TOPIC, json.dumps(msg))
    print("Reader started")
    print("Press Ctrl-C or red button to stop.")
    try:
      while 1:
        save_uid_log(["uid","test"],time.time())
        time.sleep(2)
    except KeyboardInterrupt:
        msg = {"status": "health", "on": 0, "instance_id": terminal_id}
        client.publish(QUEUE_TOPIC, json.dumps(msg))

initialize_reader()
