import common.corbomiteIo
from common.corbomiteValue import CorbomiteValue


class Widget:
    def __init__(self, device, name):
        self.device = device
        self.name = name

    def write(self, data):
        self.device.write("%s %s" % (self.name, data))


class InputWidget(Widget):
    def __init__(self, device, name, sendFunction):
        Widget.__init__(self, device, name)
        self.name = name
        self.sendFunction = sendFunction

    def onInfo(self):
        info = self.getInfo()
        if info:
            return "%s %s %s" % (self.kind, self.name, self.getInfo())
        else:
            return "%s %s" % (self.kind, self.name)

    def send(self):
        self.sendFunction()


class OutputWidget(InputWidget):
    def __init__(self, device, name, sendFunction, receiveCallbacks):
        InputWidget.__init__(self, device, name, sendFunction)
        self.receiveCallbacks = receiveCallbacks

    def receive(self, data, interface):
        for callback in self.receiveCallbacks:
            callback(data, interface)


class AnalogIn(InputWidget):
    def __init__(self, device, name, unit, minUnit, maxUnit,
                 minRaw, maxRaw, sendFunction):
        InputWidget.__init__(self, device, name, sendFunction)
        self.value = CorbomiteValue(unit, minUnit, maxUnit, minRaw, maxRaw)
        self.lastValue = self.value.minRaw
        self.kind = 'ain'

    def setRawValue(self, value):
        self.write(str(value))

    def receive(self, frame, interface):
        interface.write("%s %s" % (self.name, self.lastValue))

    def getInfo(self):
        return self.value.getInfoString()


class AnalogOut(OutputWidget):
    def __init__(self, device, name, unit, minUnit, maxUnit, minRaw, maxRaw,
                 sendFunction, receiveCallbacks=[]):
        OutputWidget.__init__(self, device, name, sendFunction,
                              receiveCallbacks)
        self.value = CorbomiteValue(unit, minUnit, maxUnit, minRaw, maxRaw)
        self.lastValue = self.value.minRaw
        self.kind = 'aout'

    def getInfo(self):
        return self.value.getInfoString()


class EventOut(OutputWidget):
    def __init__(self, device, name, receiveFunction):
        OutputWidget.__init__(self, device, name, None, receiveFunction)
        self.kind = 'eout'

    def getInfo(self):
        return None


class EventIn(InputWidget):
    def __init__(self, device, name):
        # Input event only has a write function
        InputWidget.__init__(self, device, name, None, None)
        self.kind = 'ein'

    def getInfo(self):
        return None

    def send(self):
        pass


class CorbomiteDevice(common.corbomiteIo.CorbomiteIo):
    def __init__(self, interface):
        self.widgets = []
        self.widgetDict = {}
        common.corbomiteIo.CorbomiteIo.__init__(self, interface)
        self.interface = interface
        self.addWidget(EventOut(self, 'info', [self.onInfo]))

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.widgetDict[widget.name] = widget

    def parseMessage(self, message):
        pass

    def frameReceiver(self, frame):
        name = frame.split(' ')[0]
        if name in self.widgetDict:
            self.widgetDict[name].receive(frame, self)
        else:
            print "Unable to find a widget named", name

    def onInfo(self, frame, interface):
        for w in self.widgets[1:]:
            self.write(w.onInfo())
        self.write("idle")
