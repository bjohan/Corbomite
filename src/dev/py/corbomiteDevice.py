class Widget:
    def __init__(self, name):
        self.name = name
        
    def read(self):
        pass

    def write(self):
        pass

class AnalogOut(widget):
    def __init__(self):
        pass



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
            
