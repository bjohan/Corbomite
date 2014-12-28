import corbomiteWidgets
import wx
import random
import math

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
        self.ctrlPressed = False
        self.leftPressed = False
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.sizeEvent)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.yWeight=15
        self.x = []
        self.y = []
        self.lastCoords = None
        self.pixelsPerGraticuleLine = 30
        for i in range(1000):
            self.x.append(float(i));
            self.y.append(math.sin(float(i)/100.0))
        self.autoScale()

    def autoScale(self):
        self.xMin = min(self.x)
        self.xMax = max(self.x)
        self.yMin = min(self.y)
        self.yMax = max(self.y)

    def onLeftDown(self, evt):
        self.leftPressed = True
        self.lastCoords = (evt.GetX(), evt.GetY())

    def onMotion(self, evt):
        if self.leftPressed:
            dxp = evt.GetX()-self.lastCoords[0]
            dyp = evt.GetY()-self.lastCoords[1]
            uppx = -(self.xMax-self.xMin)/float(self.GetSize()[0])
            uppy = (self.yMax-self.yMin)/float(self.GetSize()[1])
            dx = dxp*uppx
            dy = dyp*uppy
            self.xMax+=dx
            self.yMax+=dy
            self.xMin+=dx
            self.yMin+=dy
            self.onPaint(evt)
            self.lastCoords = (evt.GetX(), evt.GetY())

    def onLeftUp(self,evt):
        self.leftPressed = False
        self.lastCoords = None

    def onDoubleClick(self, evt):
        self.autoScale()
        self.onPaint(evt)          

    def onKeyDown(self, evt):
        if evt.GetKeyCode() == wx.WXK_CONTROL:
            self.ctrlPressed = True
     
    def onKeyUp(self, evt):
        if evt.GetKeyCode() == wx.WXK_CONTROL:
            self.ctrlPressed = False
     
    def zoomYScale(self, factor):
        center = 0.5*(self.yMin+self.yMax)
        half = self.yMax-center
        half = half/factor
        self.yMin = center-half
        self.yMax = center+half

    def zoomXScale(self, factor):
        center = 0.5*(self.xMin+self.xMax)
        half = self.xMax-center
        half = half/factor
        self.xMin = center-half
        self.xMax = center+half

    def onMouseWheel(self, evt):
        if evt.GetWheelRotation() < 0:
            if self.ctrlPressed:
                self.zoomXScale(1.1)
            else:
                self.zoomYScale(1.1)
        else:
            if self.ctrlPressed:
                self.zoomXScale(1/1.1)
            else:
                self.zoomYScale(1/1.1)
        self.onPaint(evt)            
        

    def sizeEvent(self, evt):
        self.Refresh()

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        self.render(dc)

    def findClosest125(self, value):
        tens = -20
        while True:
            for m in [1, 2, 5]:
                f = (10**tens)*m
                if f > value:
                    return f
            tens+=1

    def getGraticuleResolution(self, axisRange, axisSize):
        maxGraticuleLines = axisSize/self.pixelsPerGraticuleLine
        firstGuess = axisRange/maxGraticuleLines
        return self.findClosest125(firstGuess)

    def xAxisToPixels(self, x):
        (winx, winy) = self.GetSize();
        pixelsPerUnit = winx/(self.xMax-self.xMin)
        xPixels = (x-self.xMin)*pixelsPerUnit
        return xPixels
        
    def yAxisToPixels(self, y):
        (winx, winy) = self.GetSize();
        pixelsPerUnit = winy/(self.yMax-self.yMin)
        yPixels = winy-(y-self.yMin)*pixelsPerUnit
        return yPixels

    def computeScale(self, axisMax, axisMin, axisLengthInPixels):
        axisMax = float(axisMax)
        axisMin = float(axisMin)
        axisRange = axisMax - axisMin;
        graticuleResolution = self.getGraticuleResolution(axisRange, axisLengthInPixels)
        startGraticule = axisMin - axisMin%graticuleResolution
        currentGraticule = startGraticule
        gls = [] #Graticule lines as pixel coordinates
        while True:
            gls.append(currentGraticule)
            currentGraticule += graticuleResolution
            if currentGraticule > axisMax:
                break 
        return gls

    def drawScale(self, dc):
        (winx, winy) = self.GetSize()
        glsY = self.computeScale(self.yMax, self.yMin, winy)
        glsX = self.computeScale(self.xMax, self.xMin, winx) 
        for ya in glsY:
            y = self.yAxisToPixels(ya)
            dc.DrawLine(0, y, winx, y)
            dc.DrawText(str(ya), 0, y)
        for xa in glsX:
            x = self.xAxisToPixels(xa)
            dc.DrawLine(x, 0, x, winy)
            dc.DrawText(str(xa), x, 0)

    def drawPlot(self, dc):
        points = zip(self.x, self.y)
        for i in range(len(points)-1):
            p1 = points[i]
            p2 = points[i+1]
            dc.DrawLine(self.xAxisToPixels(p1[0]),self.yAxisToPixels(p1[1]),
                        self.xAxisToPixels(p2[0]),self.yAxisToPixels(p2[1]))
            
    def render(self, dc):
        c = wx.Colour(255,255,255)
        brush = wx.Brush(c, wx.SOLID)
        dc.SetBackground(brush)
        dc.Clear()
        self.drawScale(dc)
        self.drawPlot(dc)
        
types[corbomiteWidgets.TraceInWidget] = CorbomiteGuiWidgetTraceIn

def createWidget(parent, widget):
    try:
        constr = types[widget.__class__]
        return constr(parent, widget)
    except KeyError:
        print "WARNING", widget.__class__, "is not supported"

