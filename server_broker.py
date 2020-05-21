import time
import json
import paho.mqtt.client as mqtt
import db_management as dbm

QUEUE_ADDRESS="localhost"
QUEUE_TOPIC="logging"
client = mqtt.Client()
client.connect(QUEUE_ADDRESS)


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

client.on_message = consume_message
print("Started broker server")

def ​create_main_window​():   
    window.geometry(​"250x100"​)   
    window.title(​"RECEIVER"​)   
    label = tkinter.Label(window, ​text​=​"Listening to the MQTT"​)   
    exit_button = tkinter.Button(window, ​text​=​"Stop"​, ​command​=window.quit)​ 
    hello_button = tkinter.Button(window, text=​"Server started"​, command=lambda:client.publish(​"server/name"​, ​"Hello from the server"​)) #add this line
    print_log_button = tkinter.Button(window, ​text​=​"Print log"​, ​command​=print_log_to_window)   
    label.pack()​hello_button.pack(side=​"right"​)   
    exit_button.pack(​side​=​"right"​)   
    print_log_button.pack(​side​=​"right"​)

while 1:
    client.loop_start()
    client.subscribe(QUEUE_TOPIC, 2)
    time.sleep(1)
