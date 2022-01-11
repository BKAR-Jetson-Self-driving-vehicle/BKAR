import json
from flask import Flask, redirect, request, url_for, render_template
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

SYSTEM = {}
LIGHT = {}
KEY = {}
MOTOR = {}
SENSOR = {}

# Views
@app.route('/')
def Dashboard():
    return render_template('index.html')

@app.route('/Home')
def Home():
    return 'Home'

@app.route('/Main')
def Main():
    return 'Main'

@app.route('/Stream')
def streamCamera():
    return 'Camera'

@app.route('/Controller')
def configControl():
    return render_template('Controller.html')

@app.route('/Connection')
def Connection():
    return 'Connection'

@app.route('/Settings')
def Settings():
    return 'Settings'

@app.route('/Information')
def Information():
    return 'Information'

# API
class System(Resource):
    def get(self):
        return SYSTEM
    def put(self):
        return

class Control(Resource):
    def get(self):
        return KEY
    def put(self):
        return

class Stream(Resource):
    def get(self):
        return
    def put(self):
        return

class Motor(Resource):
    def get(self):
        return MOTOR
    def put(self):
        pass

class Sensor(Resource):
    def get(self):
        return SENSOR
    def put(self):
        pass

class Light(Resource):
    def get(self):
        return LIGHT
    def put(self):
        pass

api.add_resource(System, '/System')
api.add_resource(Control, '/Control')
# api.add_resource(Control, '/Stream')
api.add_resource(Motor, '/Motor')
api.add_resource(Sensor, '/Sensor')
api.add_resource(Light, '/Light')

if __name__ == '__main__':
    with open('status.json', 'r') as f:
        status = json.load(f)
        SYSTEM = status['SYSTEM']
        MOTOR = status['MOTOR']
        SENSOR = status['SENSOR']
        LIGHT = [status['LIGHT']]

    with open('KEY.json', 'r') as f:
        KEY = json.load(f)

    app.run(debug=True)