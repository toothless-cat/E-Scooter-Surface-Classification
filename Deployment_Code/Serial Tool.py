print("opening serial port...")
import serial
import time
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM15'
print(ser)
ser.dtr = None
print(ser)
ser.open()
print(ser.readline())