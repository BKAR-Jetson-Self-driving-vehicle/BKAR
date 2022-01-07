import json
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
class Status(Resource):
    def get(self):
        return {'hello': 'api'}

class Control(Resource):
    pass

class Stream(Resource):
    pass

api.add_resource(Status, '/Status')
api.add_resource(Control, '/Control')
api.add_resource(Control, '/Stream')

if __name__ == '__main__':
    app.run(debug=True)