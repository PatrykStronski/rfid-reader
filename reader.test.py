import time
import json
import uuid
import paho.mqtt.client as mqtt
import constants as consts

client = mqtt.Client()
client.tls_set("./config/ca.crt")
client.username_pw_set(username='client', password='client')
client.connect(consts.QUEUE_ADDRESS, consts.PORT)
terminal_id = str(uuid.uuid4())

def process_ack_message(client, userdata, message):
    print(message.payload.decode("utf-8"))

def save_uid_log(uid,time_read):
    s = "-"
    time_read=int(time_read)
    msg = {"status": "log", "time": time_read, "uid": s.join(uid), "instance_id": terminal_id}
    print("Sending message to server")
    client.publish(consts.QUEUE_TOPIC, json.dumps(msg))

def initialize_reader():
    msg = {"status": "health", "on": 1, "instance_id": terminal_id}
    client.publish(consts.QUEUE_TOPIC, json.dumps(msg))
    print("Reader started")
    print("Press Ctrl-C or red button to stop.")
    try:
      while 1:
        client.loop_start()
        print(consts.QUEUE_TOPIC_ACK + "/" + terminal_id)
        client.subscribe(consts.QUEUE_TOPIC_ACK + "/" + terminal_id, 2)
        save_uid_log(["uid","test"],time.time())
        time.sleep(1)
    except KeyboardInterrupt:
        msg = {"status": "health", "on": 0, "instance_id": terminal_id}
        client.publish(consts.QUEUE_TOPIC, json.dumps(msg))

client.on_message = process_ack_message
initialize_reader()