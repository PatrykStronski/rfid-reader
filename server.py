from flask import flask
from flask_restful import Resource, Api, reqparse
import db_management as dbm

app = Flask(__name__)
api = Api(app)

class Employee:
    def put(self):
        parser.add_argument("name")
        parser.add_argument("lname")
        parser.add_argument("uid")
        args = parser.parse_args()
        dbm.add_user(args["name"], args["lname"], args["uid"])
        return "ok", 200

    def get(self):
        return dbm.fetch_all_users(), 200

api.add_resource(Employee,'/employee/')

if __name__ == "__main__":
  app.run(debug=True)
