import corbomiteWidgets
import wx
import random
import math
import time

types = {}

class CorbomiteGuiWidget(wx.Panel):
    def __init__(self, parent, widget):
        wx.Panel.__init__(self, parent = parent)
        self.widget = widget
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.yWeight = 1

class CorbomiteGuiWidgetDigitalOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.box = wx.CheckBox(parent = self, label = widget.name)
        self.box.Bind(wx.EVT_CHECKBOX, self.OnClick)
        self.sizer.Add(self.box, 1, wx.GROW)

    def OnClick(self, e):
        self.widget.setValue(self.box.GetValue())

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
        self.widget.setValue(None)
types[corbomiteWidgets.EventOutWidget] = CorbomiteGuiWidgetEventOut


#class CorbomiteGuiWidgetAnalogOut(CorbomiteGuiWidget):
#    def __init__(self, parent, widget):
#        CorbomiteGuiWidget.__init__(self, parent, widget)
#        self.slider = wx.Slider(self, wx.ID_ANY, widget.value.minUnit,widget.value.minUnit, widget.value.maxUnit)
#        self.slider.Bind(wx.EVT_SLIDER, self.OnSlide)
#        self.label = wx.StaticText(self, label = self.widget.name)
#        self.spinner = wx.SpinCtrl(self, value = str(widget.value.minUnit), min = widget.value.minUnit, max = widget.value.maxUnit)
#        self.spinner.Bind(wx.EVT_SPIN, self.onSpin)
#        self.spinner.Bind(wx.EVT_TEXT, self.onSpin)
#        self.sizer.Add(self.label,1)
#        self.sizer.Add(self.spinner,1)
#        self.sizer.Add(self.slider, 3)
#    
#    def onSpin(self, e):
#        print self.widget.value.getPrecisionString(float(self.spinner.GetValue()), 5)
#        self.slider.SetValue(self.spinner.GetValue())
#        self.widget.setValue(self.spinner.GetValue())
#        self.label.SetLabel(self.widget.name+' '+self.widget.value.getPrecisionString(float(self.spinner.GetValue()), 3))
#    
#    def OnSlide(self, e):
#        self.spinner.SetValue(self.slider.GetValue())
#        self.widget.setValue(self.slider.GetValue())
#        #self.label.SetLabel(self.widget.value.getValueString())

class CorbomiteGuiWidgetAnalogOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.label = wx.StaticText(self, label = self.widget.name)
        self.valueText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.valueText)
        self.spinX1 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinX2 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinX3 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinUnit = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.Bind(wx.EVT_SPIN, self.onPrefixSpin, self.spinUnit)
        self.Bind(wx.EVT_SPIN, self.onSpinX1, self.spinX1)
        self.Bind(wx.EVT_SPIN, self.onSpinX2, self.spinX2)
        self.Bind(wx.EVT_SPIN, self.onSpinX3, self.spinX3)
        self.slider = wx.Slider(self, wx.ID_ANY, 0, 0, 1000000)
        self.slider.Bind(wx.EVT_SLIDER, self.onSlide)
        self.preferedPrefix, foo = corbomiteWidgets.calculatePrefix(self.widget.value.getUnit())
        self.updateValue(self.widget.value.minUnit)
        

        #self.slider.Bind(wx.EVT_SLIDER, self.OnSlide)
        #self.spinner = wx.SpinCtrl(self, value = str(widget.value.minUnit), min = widget.value.minUnit, max = widget.value.maxUnit)
        #self.spinner.Bind(wx.EVT_SPIN, self.onSpin)
        #self.spinner.Bind(wx.EVT_TEXT, self.onSpin)
        self.sizer.Add(self.label,4)
        self.sizer.Add(self.valueText,8)
        self.sizer.Add(self.spinX1,1)
        self.sizer.Add(self.spinX2,1)
        self.sizer.Add(self.spinX3,1)
        self.sizer.Add(self.spinUnit,1)
        self.sizer.Add(self.slider, 12)


    def onEnter(self, evt):
        text = self.valueText.GetValue()
        value = corbomiteWidgets.stringToValue(text)
        self.updateValue(value)

    def updateValue(self, value):
        self.shadowValue = value
        self.updateValueText()
        #self.widget.value.setUnit(value)
        self.widget.setValue(value)
        self.setSlider()
    
    def setSlider(self):
        sval = float(self.slider.GetMax())*float(self.shadowValue-self.widget.value.minUnit)/float(self.widget.value.maxUnit)
        self.slider.SetValue(sval)

    def spinDelta(self, spinner):
        if spinner.GetValue() > 0:
            delta = 1
        else:
            delta = -1
        print "delta", delta
        spinner.SetValue(0)
        return delta

    def onPrefixSpin(self, evt):
        self.preferedPrefix += self.spinDelta(self.spinUnit)
        self.updateValue(self.shadowValue)

    def onSpinX1(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX1)*1
        print d
        self.updateValue(self.shadowValue+d)

    def onSpinX2(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX2)*10
        self.updateValue(self.shadowValue+d)

    def onSpinX3(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX3)*100
        self.updateValue(self.shadowValue+d)


    def updateValueText(self):
        dispVal = self.shadowValue/(10**(self.preferedPrefix*3))
        dispString = str(dispVal)+' '+corbomiteWidgets.prefixLetter(self.preferedPrefix)+self.widget.value.unit
        self.valueText.SetValue(dispString)

    def onSlide(self, evt):
        self.updateValue(self.widget.value.maxUnit*float(self.slider.GetValue())/float(self.slider.GetMax()))


types[corbomiteWidgets.AnalogOutWidget] = CorbomiteGuiWidgetAnalogOut

class CorbomiteGuiWidgetAnalogIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.gauge = wx.Gauge(self, wx.ID_ANY, widget.value.maxRaw - widget.value.minRaw)
        widget.addCallback(self.update)
        self.label = wx.StaticText(self, label = self.widget.name)
        self.sizer.Add(self.label,1)
        self.sizer.Add(self.gauge, 3)

    def update(self, widget):
        self.gauge.SetValue(widget.value.getRaw())
        self.label.SetLabel(self.widget.name+' '+self.widget.value.getValueString())
        wx.Yield()

types[corbomiteWidgets.AnalogInWidget] = CorbomiteGuiWidgetAnalogIn

class CorbomiteGuiWidgetTraceIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.rightPressed = False
        self.leftPressed = False
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.onRightUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.sizeEvent)
        parent.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.yWeight=10
        self.x = []
        self.y = []
        self.lastCoords = None
        self.pixelsPerGraticuleLine = 75
        for i in range(1000):
            self.x.append(float(i));
            self.y.append(math.sin(float(i)/100.0))
        self.autoScale()
        self.widget.addCallback(self.update)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.timer.Start(200)
        self.time = time.time()

    def onTimer(self, evt):
        if time.time() > self.time:
            self.time = time.time()
            self.rePaint()

    def update(self, widget):
        if len(widget.trace) == 0:
            self.rePaint()
        self.x = []
        self.y = []
        for p in widget.trace:
            self.x.append(self.widget.value[0].toUnit(p[0]))
            self.y.append(self.widget.value[1].toUnit(p[1]))
        self.time = time.time()

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
            self.rePaint()
            self.lastCoords = (evt.GetX(), evt.GetY())

    def onLeftUp(self,evt):
        self.leftPressed = False
        self.lastCoords = None

    def onDoubleClick(self, evt):
        self.autoScale()
        self.rePaint()          

    def onRightDown(self, evt):
        self.rightPressed = True
     
    def onRightUp(self, evt):
        self.rightPressed = False
     
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
            if self.rightPressed:
                self.zoomXScale(1.1)
            else:
                self.zoomYScale(1.1)
        else:
            if self.rightPressed:
                self.zoomXScale(1/1.1)
            else:
                self.zoomYScale(1/1.1)
        self.rePaint()            
        

    def sizeEvent(self, evt):
        self.Refresh()

    def rePaint(self):
        self.render(wx.BufferedDC(wx.ClientDC(self)))

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        self.render(wx.BufferedDC(dc))

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
        
        return max(min(xPixels, winx+1), -1)
        
    def yAxisToPixels(self, y):
        (winx, winy) = self.GetSize();
        pixelsPerUnit = winy/(self.yMax-self.yMin)
        yPixels = winy-(y-self.yMin)*pixelsPerUnit
        return max(min(yPixels, winy+1), -1)

    def computeScale(self, axisMax, axisMin, axisLengthInPixels):
        axisMax = float(axisMax)
        axisMin = float(axisMin)
        axisRange = axisMax - axisMin;
        if axisRange < 1e-18:
                axisRange = 1
        graticuleResolution = self.getGraticuleResolution(axisRange, axisLengthInPixels)
        startGraticule = axisMin - axisMin%graticuleResolution
        currentGraticule = startGraticule
        gls = [] #Graticule lines as pixel coordinates
        while True:
            gls.append(currentGraticule)
            currentGraticule += graticuleResolution
            #print graticuleResolution, axisRange, axisMax, axisMin, axisLengthInPixels
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
            dc.DrawText(self.widget.value[1].getPrecisionString(ya,2), 0, y)
        for xa in glsX[1:]:
            x = self.xAxisToPixels(xa)
            dc.DrawLine(x, 0, x, winy)
            dc.DrawText(self.widget.value[0].getPrecisionString(xa,2), x, 0)
            #dc.DrawText(str(xa), x, 0)

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

