import time
import RPi.GPIO as GPIO
import MFRC522
import db_management as dbm

buttonRed = 5

def save_uid_log(uid,time_read):
    s = "-"
    time_read=int(time_read)
    dgm.save_message(s.join(uid),time_read)

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
