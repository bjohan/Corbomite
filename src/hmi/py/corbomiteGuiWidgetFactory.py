import corbomiteWidgets
import wx
import random

types = {}

class CorbomiteGuiWidget(wx.Panel):
    def __init__(self, parent, widget):
        wx.Panel.__init__(self, parent = parent)
        self.widget = widget
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.yWeight = 1

    def setValue(self, value):
        self.writeValue(value)

class CorbomiteGuiWidgetDigitalOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.box = wx.CheckBox(parent = self, label = widget.name)
        self.box.Bind(wx.EVT_CHECKBOX, self.OnClick)
        self.sizer.Add(self.box, 1, wx.GROW)

    def OnClick(self, e):
        self.widget.writeValue(self.box.GetValue())

types[corbomiteWidgets.DigitalOutWidget] = CorbomiteGuiWidgetDigitalOut

class CorbomiteGuiWidgetDigitalIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.box = wx.CheckBox(parent = self, label = widget.name)
        self.box.Enable(False)
        self.sizer.Add(self.box, 1)
        widget.addCallback(self.update)

    def update(self, widget):
        if(widget.value > 0):
            self.box.SetValue(True)
        else:
            self.box.SetValue(False)
types[corbomiteWidgets.DigitalInWidget] = CorbomiteGuiWidgetDigitalIn

class CorbomiteGuiWidgetEventOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.button = wx.Button(parent = self,  label = self.widget.name)
        self.button.Bind(wx.EVT_BUTTON, self.onButton)
        self.sizer.Add(self.button, 1)

    def onButton(self, e):
        self.widget.writeValue(None)
types[corbomiteWidgets.EventOutWidget] = CorbomiteGuiWidgetEventOut

class CorbomiteGuiWidgetAnalogOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.slider = wx.Slider(self, wx.ID_ANY, widget.minValue,widget.minValue, widget.maxValue)
        self.slider.Bind(wx.EVT_SLIDER, self.OnSlide)
        self.label = wx.StaticText(self, label = self.widget.name)
        self.sizer.Add(self.label,1)
        self.sizer.Add(self.slider, 3)
    
    def OnSlide(self, e):
        self.widget.writeValue(self.slider.GetValue())
types[corbomiteWidgets.AnalogOutWidget] = CorbomiteGuiWidgetAnalogOut

class CorbomiteGuiWidgetAnalogIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.gauge = wx.Gauge(self, wx.ID_ANY, widget.maxValue - widget.minValue)
        widget.addCallback(self.update)
        self.label = wx.StaticText(self, label = self.widget.name)
        self.sizer.Add(self.label,1)
        self.sizer.Add(self.gauge, 3)

    def update(self, widget):
        self.gauge.SetValue(widget.value)
        wx.Yield()

types[corbomiteWidgets.AnalogInWidget] = CorbomiteGuiWidgetAnalogIn

class CorbomiteGuiWidgetTraceIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.sizeEvent)
        self.yWeight=15

        for i in range(1000):
            self.x = i;
            self.y = (random.random()-0.5)*10

    def sizeEvent(self, evt):
        pass#self.Refresh()

    def onPaint(self, evt):
        print "Drawing"
        dc = wx.PaintDC(self)
        dc = wx.ClientDC(self)
        self.render(dc)

    def render(self, dc):
        c = wx.Colour(255,255,255)

        brush = wx.Brush(c, wx.SOLID)
        dc.SetBackground(brush)
        dc.Clear()
        dc.DrawLine(50,60,190,60)
        a = self.GetSize()
        dc.DrawLine(0,0,a[0],a[1])
        self.Layout()
        
types[corbomiteWidgets.TraceInWidget] = CorbomiteGuiWidgetTraceIn

def createWidget(parent, widget):
    try:
        constr = types[widget.__class__]
        return constr(parent, widget)
    except KeyError:
        print "WARNING", widget.__class__, "is not supported"

