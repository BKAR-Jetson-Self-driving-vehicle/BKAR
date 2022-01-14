import json
from flask import Flask, redirect, request, url_for, render_template
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

# =========================================
SYSTEM_ARGS_PUT_API = reqparse.RequestParser()
SYSTEM_ARGS_PUT_API.add_argument('TIMESTAMP',
                                 type=int,
                                 help='Time send request.')
SYSTEM_ARGS_PUT_API.add_argument('IP',
                                 type=str,
                                 help='IP Address of BKAR.')
SYSTEM_ARGS_PUT_API.add_argument('CONNECTED',
                                 type=bool,
                                 help='Connect status.')
SYSTEM_ARGS_PUT_API.add_argument('DISTANCE',
                                 type=int,
                                 help='Distance traveled.')
SYSTEM_ARGS_PUT_API.add_argument('VOLTAGE',
                                 type=float,
                                 help='Battery voltage.')
SYSTEM_ARGS_PUT_API.add_argument('TRAFFIC_SIGN',
                                 type=str,
                                 help='Traffic sign just met.')
SYSTEM_ARGS_PUT_API.add_argument('GEAR',
                                 type=str,
                                 help='Current gear mode.')
SYSTEM_ARGS_PUT_API.add_argument('MODE',
                                 type=str,
                                 help='Current driving mode.')

SENSOR_ARGS_PUT_API = reqparse.RequestParser()
SENSOR_ARGS_PUT_API.add_argument('X', type=float, help='X-axis.')
SENSOR_ARGS_PUT_API.add_argument('Y', type=float, help='Y-axis.')
SENSOR_ARGS_PUT_API.add_argument('Z', type=float, help='Z-axis.')

MOTOR_ARGS_PUT_API = reqparse.RequestParser()
MOTOR_ARGS_PUT_API.add_argument('SPEED',
                                type=int,
                                help='Speed of the Car.')
MOTOR_ARGS_PUT_API.add_argument('A_RATE',
                                type=float,
                                help='Rate speed of motor A.')
MOTOR_ARGS_PUT_API.add_argument('B_RATE',
                                type=float,
                                help='Rate speed of motor B.')

LIGHT_ARGS_PUT_API = reqparse.RequestParser()
LIGHT_ARGS_PUT_API.add_argument('HEAD', type=bool, help='Head light status.')
LIGHT_ARGS_PUT_API.add_argument('LEFT', type=bool, help='Left light status.')
LIGHT_ARGS_PUT_API.add_argument('RIGHT', type=bool, help='Right light status.')

CONTROL_ARGS_PUT_API = reqparse.RequestParser()
CONTROL_ARGS_PUT_API.add_argument('CONNECTED',
                                  type=bool,
                                  help='State of connection')
CONTROL_ARGS_PUT_API.add_argument('BUTTON',
                                  type=dict,
                                  help='State of all button.')
CONTROL_ARGS_PUT_API.add_argument('AXIS',
                                  type=dict,
                                  help='State of all axis.')

# =========================================
SYSTEM = {}
LIGHT = {}
KEY = {}
MOTOR = {}
SENSOR = {}


# =========================================
# Views
@app.route('/')
def Dashboard():
    return render_template('Index.html')


# =========================================
@app.route('/Welcome')
def Home():
    return render_template('Welcome.html')


@app.route('/Connection')
def Connection():
    if SYSTEM['CONNECTED']:
        return redirect(url_for('/Stream'))
    else:
        return render_template('Connection.html')


@app.route('/Demo')
def Demo():
    return 'Demo'


@app.route('/Stream')
def streamCamera():
    return 'Camera'


# =========================================
@app.route('/Controller')
def configControl():
    return render_template('Controller.html')


# =========================================
@app.route('/Settings')
def Settings():
    return 'Settings'


# =========================================
@app.route('/Information')
def Information():
    return 'Information'


# =========================================
# API
class System(Resource):
    def get(self):
        return SYSTEM

    def put(self):
        args = SYSTEM_ARGS_PUT_API.parse_args()
        for key in SYSTEM.keys():
            if args[key] is not None:
                SYSTEM[key] = args[key]
        return SYSTEM


class Control(Resource):
    def get(self):
        return KEY

    def put(self):
        args = CONTROL_ARGS_PUT_API.parse_args()
        if args['BUTTON'] is not None:
            KEY["BUTTON"] = args['BUTTON']
        if args['AXIS'] is not None:
            KEY["AXIS"] = args['AXIS']
        if args["CONNECTED"] is not None:
            KEY['CONNECTED'] = args['CONNECTED']
        return KEY


class Stream(Resource):
    def get(self):
        return

    def put(self):
        return


class Motor(Resource):
    def get(self):
        return MOTOR

    def put(self):
        args = MOTOR_ARGS_PUT_API.parse_args()
        for key in MOTOR.keys():
            if args[key] is not None:
                MOTOR[key] = args[key]
        return MOTOR


class Sensor(Resource):
    def get(self):
        return SENSOR

    def put(self):
        args = SENSOR_ARGS_PUT_API.parse_args()
        for key in SENSOR.keys():
            if args[key] is not None:
                SENSOR[key] = args[key]
        return SENSOR


class Light(Resource):
    def get(self):
        return LIGHT

    def put(self):
        args = LIGHT_ARGS_PUT_API.parse_args()
        for key in LIGHT.keys():
            if args[key] is not None:
                LIGHT[key] = args[key]
        return LIGHT


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
        LIGHT = status['LIGHT']

    with open('KEY.json', 'r') as f:
        KEY = json.load(f)

    app.run(debug=False)
