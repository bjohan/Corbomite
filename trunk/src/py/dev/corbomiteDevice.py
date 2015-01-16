class Widget:
    def __init__(self, name, readCallback, writeCallback):
        self.name = name

    def onInfo(self):
        pass
    
class AnalogIn(Widget):
    def __init__(self, iface, name, unit, minUnit, maxUnit,
                    minRaw, maxRaw, writeCallback, readCallback):
        Widget.__init__(self, name)
        self.iface = iface
        self.unit = unit
        self.minUnit = minUnit
        self.maxUnit = maxUnit
        self.minRaw = minRaw
        self.maxRaw = maxRaw
        self.writeCallback = writeCallback
        self.readCallback = readCallback

    def onInit(self):
        self.iface.writeFrame("%s %s %f %f %d %d"%(name, unit, 
                minUnit, maxUnit, minRaw, maxRaw))


class CorbomiteDevice:
    def __init__(self, interface):
        self.widgets = []
        self.widgetDict = {}
        self.interface = interface

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.widgetDict[widget.name] = widget

    def parseMessage(self, message)
        pass

    def onInfo(self):
        for w in self.widgets:
            self.interface.write(w.onInfo())
            
