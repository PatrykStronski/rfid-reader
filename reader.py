import time
import uuid
import RPi.GPIO as GPIO
import MFRC522
import paho.mqtt.client as mqtt

buttonRed = 5
QUEUE_ADDRESS="mqtt://localhost"
QUEUE_TOPIC="logging"

client = mqtt.Client()
i_id = uuid.uuid4()

def save_uid_log(uid,time_read):
    client.connect(QUEUE_ADDRESS)
    s = "-"
    time_read=int(time_read)
    msg = {time: time_read, uid: s.join(uid), instance_id: i_id}
    client.publish(QUEUE_TOPIC, msg)

def initialize_reader():
    MIFAREReader = MFRC522.MFRC522()
    print("Reader started")
    print("Press Ctrl-C or red button to stop.")
    try:
      while GPIO.input(buttonRed):
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
          save_uid_time(uid,time.time())
          print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
          time.sleep(5)
    except KeyboardInterrupt:
      GPIO.cleanup()
