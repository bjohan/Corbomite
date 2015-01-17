from com.corbomiteValue import CorbomiteValue


class CorbomiteWidget:
    types = {}

    @staticmethod
    def factory(frame, parentDevice):
        t = frame.split()[0]
        if t in CorbomiteWidget.types:
            return CorbomiteWidget.types[t](frame, parentDevice)
        else:
            print "Warning", t, "is not supported by this implementation"

    @staticmethod
    def registerCorbomiteWidgetType(t, constructor):
        CorbomiteWidget.types[t] = constructor

    def __init__(self, frame, parentDevice, value):
        self.name = frame.split()[1]
        self.parentDevice = parentDevice
        self.parentDevice.widgets[self.name] = self
        self.callBacks = []
        self.value = value

    def process(self, line):
        self.readEvent(line)
        self.callCallbacks(self)

    def setValue(self, value):
        self.value.setUnit(value)
        self.writeValue(self.value.getRaw())

    def readEvent(self, line):
        print self.__class__.__name__, "does not have a an event handler so:",\
            line, "is unprocessed"

    def addCallback(self, cbk):
        self.callBacks.append(cbk)

    def callCallbacks(self, value):
        for c in self.callBacks:
            c(value)


class AnalogInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue(toks[2], toks[3], toks[4],
                                                toks[5], toks[6]))

    def readEvent(self, line):
        self.value.setRaw(int(line.split()[1]))

CorbomiteWidget.registerCorbomiteWidgetType('ain', AnalogInWidget)


class AnalogOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue(toks[2], toks[3], toks[4],
                                                toks[5], toks[6]))

    def writeValue(self, value):
        self.parentDevice.write(self.name+' '+str(value))
CorbomiteWidget.registerCorbomiteWidgetType('aout', AnalogOutWidget)


class DigitalInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue('bool', 0, 1, 0, 1))

    def readEvent(self, line):
        self.value = int(line.split()[1])

CorbomiteWidget.registerCorbomiteWidgetType('din', DigitalInWidget)


class DigitalOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue('bool', 0, 1, 0, 1))

    def writeValue(self, value):
        valueToSend = ' 0'
        if value is True or value > 0:
            valueToSend = ' 1'
        self.parentDevice.write(self.name+valueToSend)

CorbomiteWidget.registerCorbomiteWidgetType('dout', DigitalOutWidget)


class TraceInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 [CorbomiteValue(toks[2], toks[3], toks[4],
                                                 toks[5], toks[6]),
                                  CorbomiteValue(toks[7], toks[8], toks[9],
                                                 toks[10], toks[11])])
        self.trace = []
        self.x = None
        self.y = None

    def readEvent(self, line):
        try:
            tokens = line.split()
            self.x = int(tokens[1])
            self.y = int(tokens[2])
            if len(self.trace) > 0:
                if self.trace[-1][0] > self.x:
                    self.trace = []
            self.trace.append((self.x, self.y))
        except:
            print "Unable to parse the line", line

CorbomiteWidget.registerCorbomiteWidgetType('tin', TraceInWidget)


class TraceOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('tout', TraceOutWidget)


class EventInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue('event', 0, 1, 0, 1))
CorbomiteWidget.registerCorbomiteWidgetType('ein', EventInWidget)


class EventOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue('event', 0, 1, 0, 1))

    def setValue(self, value):
        self.writeValue(None)

    def writeValue(self, value):
        self.parentDevice.write(self.name)

CorbomiteWidget.registerCorbomiteWidgetType('eout', EventOutWidget)


class InfoWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,
                                 CorbomiteValue('str', 0, 1, 0, 1))

CorbomiteWidget.registerCorbomiteWidgetType('info', InfoWidget)
