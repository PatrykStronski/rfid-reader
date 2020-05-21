import time
import json
import uuid
import RPi.GPIO as GPIO
import MFRC522
import paho.mqtt.client as mqtt
import tkinter

buttonRed = 5
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
    client.publish(QUEUE_TOPIC, json.dumps(msg))

def initialize_reader():
    MIFAREReader = MFRC522.MFRC522()
    msg = {"status": "health", "on": 1, "instance_id": terminal_id}
    client.publish(QUEUE_TOPIC, json.dumps(msg))
    print("Reader started")
    print("Press Ctrl-C or red button to stop.")
    try:
      while GPIO.input(buttonRed):
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
          save_uid_time(uid,time.time())
          print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
          time.sleep(1)
    except KeyboardInterrupt:
        msg = {"status": "health", "on": 0, "instance_id": terminal_id}
        client.publish(QUEUE_TOPIC, json.dumps(msg))
        GPIO.cleanup()
