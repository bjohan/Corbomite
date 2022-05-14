import math


def calculatePrefix(value):
        if abs(value) < 1e-21:
            return (0, '')
        decades = math.log10(abs(value))
        prefNum = int(int(decades)/3)
        prefix = 'afnpum KMGTPY'[prefNum + 6]
        return (prefNum, prefix)


def prefixLetter(prefNum):
        return 'afnpum KMGTPY'[prefNum + 6]


def calculatePrefixMultiplier(prefix):
        return 10**(('afnpum KMGTPY'.index(prefix)-6)*3)


def stringToValue(st):
        i = 0
        decCount = 0
        for s in st:
            i += 1
            if s not in ['1', '2', '3', '4', '5', '6',
                         '7', '8', '9', '0', '.', ',']:
                break
            if s in ['.', ',']:
                decCount += 1
                if decCount > 1:
                    break
        number = st[0:i-1]
        p = st[i-1:].strip()[0]
        print("number", number, decCount)
        try:
            return float(number)*calculatePrefixMultiplier(p)
        except:
            return float(number)


class CorbomiteValue:
    def __init__(self, unit, minUnit, maxUnit, minRaw, maxRaw):
        self.setParameters(unit, minUnit, maxUnit, minRaw, maxRaw)

    def setParameters(self, unit, minUnit, maxUnit, minRaw, maxRaw):
        self.unit = unit
        self.minUnit = float(minUnit)
        self.maxUnit = float(maxUnit)
        self.minRaw = int(minRaw)
        self.maxRaw = int(maxRaw)
        self.unitsPerRaw = (self.maxUnit - self.minUnit) /\
                           (self.maxRaw - self.minRaw)
        self.rawValue = self.minRaw

    def getPrecisionString(self, value, precision):
        if abs(value) < 1e-21:
            return "0 " + self.unit
        decades = math.log10(abs(value))
        prefNum = int(int(decades)/3)
        prefix = 'afnpum KMGTPY'[prefNum+6]
        displayValue = value*10**(-3*prefNum)
        fmtString = '%1.'+str(precision)+'f '+str(prefix)+self.unit
        return fmtString % (displayValue)

    def getValueString(self):
        return self.getPrecisionString(self.getUnit(), 3)

    def setRaw(self, raw):
        self.rawValue = raw

    def setUnit(self, unit):
        self.rawValue = self.toRaw(unit)

    def getRaw(self):
        return int(self.rawValue)

    def getUnit(self):
        return self.toUnit(self.rawValue)

    def toUnit(self, raw):
        return self.minUnit + (raw-self.minRaw)*self.unitsPerRaw

    def toRaw(self, unit):
        return round((unit-self.minUnit)/self.unitsPerRaw + self.minRaw)

    def getUnitString(self):
        return str(self.getUnit())+' '+self.unit

    def getInfoString(self):
        return "%s %f %f %d %d" % (self.unit, self.minUnit, self.maxUnit,
                                   self.minRaw, self.maxRaw)

    def parseString(self, string):
        words = string.split(' ')
        self.setParameters(words[0], words[1], words[2], words[3], words[4])
