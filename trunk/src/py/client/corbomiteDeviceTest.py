import corbomiteDevice
import serial

port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)


fb = corbomiteDevice.CorbomiteDevice(port)
refFrame = "Hello \#there"
print "closing port"
port.close()
print "Port closed"
exit()
