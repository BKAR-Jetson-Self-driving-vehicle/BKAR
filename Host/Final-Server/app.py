import json
import re
from flask import Flask, redirect, request, url_for, render_template
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)

# Views
@app.route('/')
def Dashboard():
    return render_template('index.html')

@app.route('/Camera')
def streamCamera():
    return 'Camera'

@app.route('/ConfigControl')
def configControl():
    return 'Config Gamepad/Joystick Control'

@app.route('/ConfigConnection')
def configConnection():
    return 'ConfigConnection'

@app.route('/StartConnection')
def startConnection():
    return 'Start connection'

# API
class System(Resource):
    def get(self):
        with open('./status.json') as f:
            data = json.load(f)
            return data['SYSTEM']
    def put(self):
        return

class Control(Resource):
    def get(self):
        return

class Stream(Resource):
    pass

class Motor(Resource):
    def get(self):
        with open('./status.json') as f:
            data = json.load(f)
            return data['MOTOR']

class Sensor(Resource):
    def get(self):
        with open('./status.json') as f:
            data = json.load(f)
            return data['SENSOR']
    def put(self):
        pass

class Light(Resource):
    def get(self):
        return

api.add_resource(System, '/System')
api.add_resource(Control, '/Control')
# api.add_resource(Control, '/Stream')
api.add_resource(Motor, '/Motor')
api.add_resource(Sensor, '/Sensor')
api.add_resource(Light, '/Light')

if __name__ == '__main__':
    app.run(debug=True)