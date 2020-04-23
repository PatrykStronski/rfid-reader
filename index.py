import json
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import db_management as dbm

QUEUE_ADDRESS="localhost"
QUEUE_TOPIC="logging"
app = Flask(__name__)
client = mqtt.Client()
client.connect(QUEUE_ADDRESS)
client.loop_start()
client.subscribe(QUEUE_TOPIC, 2)

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

@app.route('/employee',methods=['PUT','GET','PATCH','DELETE'])
def employee():
    if request.method == 'PUT':
        data=request.form
        if data["u_name"] and data["l_name"] and data["uid"]:
            dbm.add_user(request.form["u_name"], request.form["l_name"], request.form["uid"])
            return "ok", 200
        else:
            return "wrong data", 400
    elif request.method == 'GET':
        return jsonify(dbm.fetch_all_users()), 200
    elif request.method == 'PATCH':
        data=request.form
        if data["e_id"] or data["e_id"] == 0:
            dbm.patch_user_card(data["e_id"], data["uid"])
            return "ok", 200
        else:
            return "no id given", 400
    elif request.method == 'DELETE':
        e_id = request.form['e_id']
        if e_id or e_id==0:
            dbm.delete_user(e_id)
        return "deleted", 200
    else:
        return "Wrong endpoint", 404

@app.route('/log_times_employee',methods=['GET'])
def get_log_times():
    employee_id=request.args['id']
    if employee_id or employee_id==0:
        return jsonify(dbm.fetch_working_times(employee_id))

@app.route('/health-check', methods=['GET'])
def health_check():
    return "health ok", 200

if __name__ == "__main__":
  app.run(debug=True)

