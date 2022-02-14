import time
from utils.Serial import Serial
from utils.Server import ConnectServer
from utils.System import MOTOR, LIGHT

mySerial = Serial()
myServer = ConnectServer()
mySerial.start()
myServer.start()

myMOTOR = MOTOR(mySerial, myServer)
myMOTOR.start()

for i in range(5):
    print(i)
    myMOTOR.setStatus([1, 1], -200)
    time.sleep(0.5)
    myMOTOR.setStatus([1, 1], -200)
    time.sleep(0.5)

myMOTOR.setStatus([1, 1], 0)
