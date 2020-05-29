# pip3 install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
# python3 flask_main.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
import os, requests, json
from flask_api import api, db
from flask_site import site


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'avimeetrensai'
# Update HOST and PASSWORD appropriately.
HOST = "35.201.6.76"
USER = "user1"
PASSWORD = "password"
DATABASE = "carrental"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)


if __name__ == "__main__":
    app.run(host = "localhost", port=8080, debug=True)

'''
#change the ip to the raspberrypi's ip. For me '0.0.0.0' is not working on local machine.
if __name__ == "__main__":
    app.run(host = "192.168.1.114", port=8080, debug=True)
'''
