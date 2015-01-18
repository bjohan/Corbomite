import device.corbomiteDevice
import sys
import time
import common.tcpCommunication


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
        self.testAnalog = device.corbomiteDevice.AnalogIn('analogtestsignal',
                                                          'V', 0.0, 1.0, 0,
                                                          1024,
                                                          [self.readAnalog])
        self.addWidget(self.testAnalog)
        self.testEvent = device.corbomiteDevice.EventOut('tja',
                                                         [self.sayHello])
        self.addWidget(self.testEvent)
        self.addWidget(device.corbomiteDevice.EventOut('bye', [self.onBye]))

    def onBye(self, msg, interface):
        print "Quitting"
        sys.exit()

    def readAnalog(self, msg):
        return str(3.1415)

    def sayHello(self, msg, interface):
        print "HEEEEELLLLOOOOO"
        interface.write("HELLO")

rw = common.tcpCommunication.TcpServer()
# rw = ReadWrite(sys.stdin, sys.stdout)
td = TestDevice(rw)

time.sleep(1000)
