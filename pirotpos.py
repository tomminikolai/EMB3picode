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
vl = 0
vr = 0
vlo = 0
vro = 0
running = True
while running:
    try:
        startmsg = ser.read(1)
        if startmsg == b'\x0F':
            mtr1 += int.from_bytes(ser.read(2), "big", signed=True)
        elif startmsg == b'\xF0':
            mtr2 += int.from_bytes(ser.read(2), "big", signed=True)
        if i >= 10:
            i = 0
            theta += (mtr1 - mtr2) / 12
            dx = ((mtr1 + mtr2) / 2) * math.cos(theta)
            dy = ((mtr1 + mtr2) / 2) * math.sin(theta)
            print(dx, dy)
            pos[0] += dx
            pos[1] += dy
            dx = 0
            dy = 0
            mtr1 = 0
            mtr2 = 0
        clientsocket.send(int(pos[0]).to_bytes(4, "big"))
        clientsocket.send(int(pos[1]).to_bytes(4, "big"))
        vl = int.from_bytes(clientsocket.recv(2), "big", signed=True)
        vr = int.from_bytes(clientsocket.recv(2), "big", signed=True)
        i += 1
        if vl != vlo or vr != vro:
            print(vl, vr)
    except KeyboardInterrupt:
        running = False
ser.close()
