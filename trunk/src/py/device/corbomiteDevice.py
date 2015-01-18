import common.corbomiteIo
import common.corbomiteValue


class InputWidget():
    def __init__(self, name, sendFunction):
        self.name = name
        self.sendFunction = sendFunction

    def onInfo(self):
        info = self.getInfo()
        if info:
            return "%s %s" % (self.name, self.getInfo())
        else:
            return self.name

    def send(self):
        self.sendFunction()


class OutputWidget(InputWidget):
    def __init__(self, name, sendFunction, receiveCallbacks):
        InputWidget.__init__(self, name, sendFunction)
        self.receiveCallbacks = receiveCallbacks

    def receive(self, data, interface):
        for callback in self.receiveCallbacks:
            callback(data, interface)


class AnalogIn(InputWidget):
    def __init__(self, name, unit, minUnit, maxUnit,
                 minRaw, maxRaw, sendFunction):
        InputWidget.__init__(self, name, sendFunction)
        self.value = common.corbomiteValue.CorbomiteValue(unit, minUnit,
                                                          maxUnit, minRaw,
                                                          maxRaw)
        self.lastValue = self.value.minRaw

    def receive(self, frame, interface):
        interface.write("%s %s" % (self.name, self.lastValue))

    def getInfo(self):
        return self.value.getInfoString()


class EventOut(OutputWidget):
    def __init__(self, name, receiveFunction):
        OutputWidget.__init__(self, name, None, receiveFunction)

    def getInfo(self):
        return None


class EventIn(InputWidget):
    def __init__(self, name):
        # Input event only has a write function
        InputWidget.__init__(self, name, None, None)

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
        self.addWidget(EventOut('info', [self.onInfo]))

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
