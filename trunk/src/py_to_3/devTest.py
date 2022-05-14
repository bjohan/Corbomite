import device.corbomiteDevice
import time
import common.tcpCommunication
from device.corbomiteDevice import AnalogIn, AnalogOut, EventOut, DigitalOut,\
    DigitalIn, TraceIn


class ReadWrite:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def read(self):
        d = self.reader.read(1)

        if d == '\n':
            return '\r\n'
        return d

    def write(self, data):
        return self.writer.write(data)


class TestDevice(device.corbomiteDevice.CorbomiteDevice):
    def __init__(self, iface):
        device.corbomiteDevice.CorbomiteDevice.__init__(self, iface)
        self.testAnalogIn = AnalogIn(self, 'aintest', 'V', 0.0, 1.0, 0,
                                     1024)
        self.addWidget(self.testAnalogIn)
        self.analogOut = AnalogOut(self, 'aouttest', 'V', 0, 1, 0, 1024,
                                   [self.receiveAout])
        self.addWidget(self.analogOut)
        self.testEvent = EventOut(self, 'tja', [self.sayHello])
        self.addWidget(self.testEvent)

        self.digitalOut = DigitalOut(self, "dot", [self.receiveDout])
        self.addWidget(self.digitalOut)

        self.digitalIn = DigitalIn(self, "di")
        self.addWidget(self.digitalIn)

        self.traceIn = TraceIn(self, "ti", "S", 0.0, 10.0, 0, 1024,
                               "V", 0.0, 10.0, 0, 1024)
        self.addWidget(self.traceIn)

    def receiveDout(self, data, interface):
        print("Recv", data)
        value = int(data.split()[1]) != 0
        self.digitalIn.setValue(value)

    def receiveAout(self, data, interface):
        print("Recv", data)
        value = int(data.split()[1])
        self.testAnalogIn.setRawValue(value)
        return str(3)

    def sayHello(self, msg, interface):
        print("HEEEEELLLLOOOOO")
        interface.write("HELLO")
        self.traceIn.setValue((0, 0))
        self.traceIn.setValue((0.50, 0.5))
        self.traceIn.setValue((1, 0))

rw = common.tcpCommunication.TcpServer()
# rw = ReadWrite(sys.stdin, sys.stdout)
td = TestDevice(rw)

time.sleep(1000)
