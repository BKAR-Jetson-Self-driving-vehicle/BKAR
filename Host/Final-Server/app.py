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

@app.route('/Stream')
def streamCamera():
    return 'Camera'

@app.route('/Controller')
def configControl():
    return render_template('Controller.html')

@app.route('/Connection')
def Connection():
    return 'Connection'

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
        with open('./KEY.json') as f:
            data = json.load(f)
            return data
    def put(self):
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
        with open('./status.json') as f:
            data = json.load(f)
            return data['LIGHT']

api.add_resource(System, '/System')
api.add_resource(Control, '/Control')
# api.add_resource(Control, '/Stream')
api.add_resource(Motor, '/Motor')
api.add_resource(Sensor, '/Sensor')
api.add_resource(Light, '/Light')

if __name__ == '__main__':
    app.run(debug=True)