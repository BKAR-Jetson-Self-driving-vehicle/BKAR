from flask import Flask, redirect, request, url_for, render_template
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)