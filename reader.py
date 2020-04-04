import time
import RPi.GPIO as GPIO
import MFRC522
import db_management as dbm


def save_uid_log(uid,time_read):
    s = "-"
    time_read=int(time_read)
    dgm.save_message(s.join(uid),time_read)

def initialize_reader():
    MIFAREReader = MFRC522.MFRC522()
    print("Looking for cards")
    print("Press Ctrl-C to stop.")
    try
      while True:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
          # Print UID
          save_uid_time(uid,time.time())
          print("UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
          time.sleep(2)
    except KeyboardInterrupt:
      GPIO.cleanup()
