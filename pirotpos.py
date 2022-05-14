import serial
import time
import socket
import math

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
clientsocket, address = s.accept()
print(f"connection from {address} has been achieved")
clientsocket.send(b'\x0F')
try:
    ser = serial.Serial("COM3")
except serial.serialutil.SerialException:
    print("not com3")
try:
    ser = serial.Serial("/dev/ttyUSB0", timeout=0.25)
except serial.serialutil.SerialException:
    print("not com5")
mtr1 = 0
mtr2 = 0
to = 0
i = 0
pos = [750, 500]
theta = 0
running = True
while running:
    try:
        startmsg = ser.read(1)
        if startmsg == b'\x0F':
            mtr1 += ser.read(2)
        elif startmsg == b'\xF0':
            mtr2 += ser.read(2)
        if i >= 10:
            i = 0
            theta += (mtr1 - mtr2) / 12
            dx = ((mtr1 + mtr2) / 2) * math.cos(theta)
            dy = ((mtr1 + mtr2) / 2) * math.sin(theta)
            pos[0] += dx
            pos[1] += dy
            clientsocket.send(int(pos[0]).to_bytes(4, "big"))
            clientsocket.send(int(pos[1]).to_bytes(4, "big"))
            mtr1 = 0
            mtr2 = 0
        i += 1
    except KeyboardInterrupt:
        running = False
ser.close()
