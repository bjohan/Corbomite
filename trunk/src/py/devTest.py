import dev.corbomiteDevice
import sys
import time


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


class TestDevice(dev.corbomiteDevice.CorbomiteDevice):
    def __init__(self, iface):
        dev.corbomiteDevice.CorbomiteDevice.__init__(self, iface)
        self.testAnalog = dev.corbomiteDevice.AnalogIn('analogtestsignal',
                                                       'V', 0.0, 1.0, 0, 1024,
                                                       [self.readAnalog])
        self.addWidget(self.testAnalog)
        self.testEvent = dev.corbomiteDevice.EventOut('tja', [self.sayHello])
        self.addWidget(self.testEvent)

    def readAnalog(self, msg):
        return str(3.1415)

    def sayHello(self, msg):
        print "HEEEEELLLLOOOOO"
rw = ReadWrite(sys.stdin, sys.stdout)
td = TestDevice(rw)

time.sleep(1000)
