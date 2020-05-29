import time
import json
import uuid
import paho.mqtt.client as mqtt
import MFRC522
import constants as consts

client = mqtt.Client()
client.tls_set("./config/ca.crt")
client.username_pw_set(username='client', password='client')
client.connect(consts.QUEUE_ADDRESS, consts.PORT)
TERMINAL_ID = str(uuid.uuid4())

def process_ack_message(cl, userdata, message):
    print(message.payload.decode("utf-8"))

def save_uid_log(uid, time_read):
    s = "-"
    time_read = int(time_read)
    msg = {"status": "log", "time": time_read, "uid": s.join(uid), "instance_id": TERMINAL_ID}
    print("Sending message to server")
    client.publish(consts.QUEUE_TOPIC, json.dumps(msg))

def initialize_reader():
    mifrc_reader = MFRC522.MFRC522()
    msg = {"status": "health", "on": 1, "instance_id": TERMINAL_ID}
    client.publish(consts.QUEUE_TOPIC, json.dumps(msg))
    print("Reader started")
    print("Press Ctrl-C or red button to stop.")
    try:
        while 1:
            (status, tag_type) = mifrc_reader.MFRC522_Request(mifrc_reader.PICC_REQIDL)
            (status, uid) = mifrc_reader.MFRC522_Anticoll()
            client.loop_start()
            client.subscribe(consts.QUEUE_TOPIC_ACK + "/" + TERMINAL_ID, 2)
            if status == mifrc_reader.MI_OK:
                save_uid_log(uid, time.time())
                print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                time.sleep(1)   
    except KeyboardInterrupt:
        msg = {"status": "health", "on": 0, "instance_id": TERMINAL_ID}
        client.publish(consts.QUEUE_TOPIC, json.dumps(msg))

client.on_message = process_ack_message
initialize_reader()
