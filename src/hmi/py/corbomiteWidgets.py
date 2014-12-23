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

    def __init__(self, frame, parentDevice):
        self.name = frame.split()[1]
        self.parentDevice = parentDevice
        self.parentDevice.widgets[self.name] = self
        self.callBacks = []
        self.value = None


    def process(self, line):
        self.readEvent(line)
        self.callCallbacks(self)

    def setValue(self, value):
        self.writeValue(value)

    def readEvent(self, line):
        print self.__class__.__name__, "does not have a an event handler so:", line, "is unprocessed"

    def addCallback(self, cbk):
        self.callBacks.append(cbk)

    def callCallbacks(self, value):
        for c in self.callBacks:
            c(value)

class AnalogInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        self.name = toks[1]
        self.unit = toks[2]
        self.minUnit = toks[3]
        self.maxUnit = toks[4]
        self.minValue = int(toks[5])
        self.maxValue = int(toks[6])
        CorbomiteWidget.__init__(self, frame, parentDevice)

    def readEvent(self, line):
        self.value = int(line.split()[1])

CorbomiteWidget.registerCorbomiteWidgetType('ain', AnalogInWidget)


class AnalogOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        self.name = toks[1]
        self.unit = toks[2]
        self.minUnit = toks[3]
        self.maxUnit = toks[4]
        self.minValue = int(toks[5])
        self.maxValue = int(toks[6])
        CorbomiteWidget.__init__(self, frame, parentDevice)

    def writeValue(self, value):
        self.parentDevice.write(self.name+' '+str(value))

CorbomiteWidget.registerCorbomiteWidgetType('aout', AnalogOutWidget)

class DigitalInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

    def readEvent(self,line):
        self.value = int(line.split()[1])

CorbomiteWidget.registerCorbomiteWidgetType('din', DigitalInWidget)


class DigitalOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

    def writeValue(self, value):
        valueToSend = ' 0'
        if(value == True or value > 0):
            valueToSend = ' 1'
        self.parentDevice.write(self.name+valueToSend)

CorbomiteWidget.registerCorbomiteWidgetType('dout', DigitalOutWidget)


class TraceInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('tin', TraceInWidget)


class TraceOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('tout', TraceOutWidget)


class EventInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('ein', EventInWidget)


class EventOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)
    def writeValue(self, value):
        self.parentDevice.write(self.name)

CorbomiteWidget.registerCorbomiteWidgetType('eout', EventOutWidget)
 
class InfoWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('info', InfoWidget)
 
