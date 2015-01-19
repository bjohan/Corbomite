import common.corbomiteIo
from common.corbomiteValue import CorbomiteValue


class Widget:
    def __init__(self, device, name):
        self.device = device
        self.name = name

    def write(self, data):
        self.device.write("%s %s" % (self.name, data))

    def onInfo(self):
        info = self.getInfo()
        if info:
            return "%s %s %s" % (self.kind, self.name, self.getInfo())
        else:
            return "%s %s" % (self.kind, self.name)

    def valueToSendString(self):
        print "Unimplemented conversion from value to send string"

    def send(self):
        self.device.write("%s %s" % (self.name, self.valueToSendString()))


class InputWidget(Widget):
    def __init__(self, device, name):
        Widget.__init__(self, device, name)
        self.name = name

    def assignValue(self, value):
        print "Assign value not implemented"

    def setValue(self, value):
        self.assignValue(value)
        self.send()


class OutputWidget(Widget):
    def __init__(self, device, name, receiveCallbacks):
        Widget.__init__(self, device, name)
        self.receiveCallbacks = receiveCallbacks

    def receive(self, data, interface):
        print "Receive callback in", self.name
        for callback in self.receiveCallbacks:
            callback(data, interface)


class AnalogIn(InputWidget):
    def __init__(self, device, name, unit, minUnit, maxUnit,
                 minRaw, maxRaw):
        InputWidget.__init__(self, device, name)
        self.value = CorbomiteValue(unit, minUnit, maxUnit, minRaw, maxRaw)
        self.valueToSend = self.value.minRaw
        self.kind = 'ain'

    def setRawValue(self, value):
        self.value.setRaw(int(value))
        self.valueToSend = self.value.getRaw()
        self.send()

    def valueToSendString(self):
        return str(self.valueToSend)

    def assignValue(self, value):
        self.value.setUnit(value)
        self.valueToSend = self.value.getRaw()

    def getInfo(self):
        return self.value.getInfoString()


class AnalogOut(OutputWidget):
    def __init__(self, device, name, unit, minUnit, maxUnit, minRaw, maxRaw,
                 receiveCallbacks=[]):
        OutputWidget.__init__(self, device, name, receiveCallbacks)
        self.value = CorbomiteValue(unit, minUnit, maxUnit, minRaw, maxRaw)
        self.lastValue = self.value.minRaw
        self.kind = 'aout'

    def addReceiver(self, receiveCallback):
        self.receiveCallbacks.append(receiveCallback)

    def getInfo(self):
        return self.value.getInfoString()


class EventOut(OutputWidget):
    def __init__(self, device, name, receiveCallbacks):
        OutputWidget.__init__(self, device, name, receiveCallbacks)
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


class DigitalIn(InputWidget):
    def __init__(self, device, name):
        InputWidget.__init__(self, device, name)
        self.valueToSend = False
        self.kind = 'din'

    def valueToSendString(self):
        if self.valueToSend:
            return "1"
        return "0"

    def assignValue(self, value):
        self.valueToSend = (value != 0)

    def getInfo(self):
        return None


class DigitalOut(OutputWidget):
    def __init__(self, device, name, receiveCallbacks=[]):
        OutputWidget.__init__(self, device, name, receiveCallbacks)
        self.kind = 'dout'

    def addReceiver(self, receiveCallback):
        self.receiveCallbacks.append(receiveCallback)

    def getInfo(self):
        return None


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
