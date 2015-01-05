import math

class CorbomiteValue:
    def __init__(self, unit, minUnit, maxUnit, minRaw, maxRaw):
        self.unit = unit
        try:
            self.minUnit = float(minUnit)
        except E:
            print E
        self.maxUnit = float(maxUnit)
        self.minRaw = float(minRaw)
        self.maxRaw = float(maxRaw)
        self.unitsPerRaw = (self.maxUnit - self.minUnit)/(self.maxRaw - self.minRaw)
        self.rawValue = None

    def getPrecisionString(self, value, precision):
        if value == 0:
            return "0 "+self.unit
        decades = math.log10(abs(value))
        prefNum = int(decades)/3;
        prefix = 'afnpum KMGTPY'[prefNum+6]
        displayValue = value*10**(-3*prefNum)
        fmtString = '%1.'+str(precision)+'f '+str(prefix)+self.unit
        return fmtString%(displayValue)

    def getValueString(self):
        return self.getPrecisionString(self.getUnit(),3)

    def setRaw(self, raw):
        self.rawValue = raw

    def setUnit(self, unit):
        self.rawValue = self.toRaw(unit)

    def getRaw(self):
        return self.rawValue

    def getUnit(self):
        return self.toUnit(self.rawValue)

    def toUnit(self, raw): 
        return self.minUnit + (raw-self.minRaw)*self.unitsPerRaw

    def toRaw(self, unit):
        return (unit-self.minUnit)/self.unitsPerRaw + self.minRaw

    def getUnitString(self):
        return str(self.getUnit())+' '+self.unit

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
        #self.value = CorbomiteValue(toks[2], toks[3], toks[4], toks[5], toks[6])
        #print "Created value", self.value
        #self.name = toks[1]
        #self.unit = toks[2]
        #self.minUnit = toks[3]
        #self.maxUnit = toks[4]
        #self.minRaw = int(toks[5])
        #self.maxRaw = int(toks[6])
        #self.unitConverter = UnitConverter(self.unit, self.minUnit, self.maxUnit, self.minRaw, self.maxRaw)
        CorbomiteWidget.__init__(self, frame, parentDevice, 
                        CorbomiteValue(toks[2], toks[3], toks[4], toks[5], toks[6]))

    def readEvent(self, line):
        self.value.setRaw(int(line.split()[1]))

CorbomiteWidget.registerCorbomiteWidgetType('ain', AnalogInWidget)


class AnalogOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        #self.name = toks[1]
        #self.unit = toks[2]
        #self.minUnit = toks[3]
        #self.maxUnit = toks[4]
        #self.minRaw = int(toks[5])
        #self.maxRaw = int(toks[6])
        CorbomiteWidget.__init__(self, frame, parentDevice,
                        CorbomiteValue(toks[2], toks[3], toks[4], toks[5], toks[6]))

    def writeValue(self, value):
        self.parentDevice.write(self.name+' '+str(value))

CorbomiteWidget.registerCorbomiteWidgetType('aout', AnalogOutWidget)

class DigitalInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice, CorbomiteValue('bool',0,1,0,1))

    def readEvent(self,line):
        self.value = int(line.split()[1])

CorbomiteWidget.registerCorbomiteWidgetType('din', DigitalInWidget)


class DigitalOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice, CorbomiteValue('bool',0,1,0,1))

    def writeValue(self, value):
        valueToSend = ' 0'
        if(value == True or value > 0):
            valueToSend = ' 1'
        self.parentDevice.write(self.name+valueToSend)

CorbomiteWidget.registerCorbomiteWidgetType('dout', DigitalOutWidget)


class TraceInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        toks = frame.split()
        CorbomiteWidget.__init__(self, frame, parentDevice, 
                        [CorbomiteValue(toks[2], toks[3], toks[4], toks[5], toks[6]),
                        CorbomiteValue(toks[7], toks[8], toks[9], toks[10], toks[11])])
        self.trace = []
        self.x = None
        self.y = None

    def readEvent(self, line):
        tokens = line.split()
        self.x = int(tokens[1])
        self.y = int(tokens[2])
        if len(self.trace) > 0:
            if self.trace[-1][0] > self.x:
                self.trace = []
        self.trace.append((self.x,self.y))

CorbomiteWidget.registerCorbomiteWidgetType('tin', TraceInWidget)


class TraceOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice)

CorbomiteWidget.registerCorbomiteWidgetType('tout', TraceOutWidget)


class EventInWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice, CorbomiteValue('event',0,1,0,1))

CorbomiteWidget.registerCorbomiteWidgetType('ein', EventInWidget)


class EventOutWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice,CorbomiteValue('event',0,1,0,1))
    def writeValue(self, value):
        self.parentDevice.write(self.name)

CorbomiteWidget.registerCorbomiteWidgetType('eout', EventOutWidget)
 
class InfoWidget(CorbomiteWidget):
    def __init__(self, frame, parentDevice):
        CorbomiteWidget.__init__(self, frame, parentDevice, CorbomiteValue('str',0,1,0,1))

CorbomiteWidget.registerCorbomiteWidgetType('info', InfoWidget)
 
