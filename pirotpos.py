import serial
import time
import socket


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
running = True
while running:
    try:
        startmsg = ser.read(1)
        if startmsg == b'\x0F':
            d1 = int.from_bytes(ser.read(2), "big", signed=True)
            mtr1 += d1
        elif startmsg == b'\xF0':
            d2 = int.from_bytes(ser.read(2), "big", signed=True)
            mtr2 += d2
        tc = time.time()
        if tc - to > 0.5:
            clientsocket.send(mtr1.to_bytes(4, "big"))
            clientsocket.send(mtr2.to_bytes(4, "big"))
            to = tc
    except KeyboardInterrupt:
        running = False
ser.close()
