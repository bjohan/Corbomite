from client import corbomiteWidgets
import wx
import time
import csv
import common.corbomiteValue
from collections import OrderedDict
types = {}


# WHARRRR!! Teh horror is horrible here!! :/
def resample(t1, x):
    """Resample traces, t1 is a tuple with (x, y) t2 is a list of points
       this function returns a trace (Tuple4 with x and y) with values at
       the points in t1[0] and x2"""
    x2 = x[:]
    rStart = max(t1[0][0], x2[0])
    rStop = min(t1[0][-1], x2[-1])
    i1 = 0
    i2 = 0
    x1 = t1[0]
    xp = rStart
    cpy = False
    resampled = ([], [])
    xp = min(t1[0][0], x2[0])
    x2.insert(0, x2[0]-1)   # Ugly fix to make sure that first value in x2 is
    # not skipped

    while True:
        if (xp >= rStart) and (xp <= rStop):
            if cpy:
                resampled[0].append(xp)
                resampled[1].append(t1[1][i1])
            else:
                sf = (xp - x1[i1])/(x1[i1+1] - x1[i1])
                yd = (t1[1][i1+1]-t1[1][i1])*sf
                ynew = t1[1][i1]+yd
                resampled[0].append(xp)
                resampled[1].append(ynew)

        if i1 + 1 == len(x1) or i2 + 1 == len(x2):
            break

        if x1[i1+1] < x2[i2+1]:
            i1 += 1
            xp = x1[i1]
            cpy = True
        elif x2[i2+1] < x1[i1+1]:
            i2 += 1
            xp = x2[i2]
            cpy = False
        else:  # x1 and x2 are equal
            i1 += 1
            i2 += 1
            xp = x1[i1]
            cpy = True

        if x1[i1] > rStop and x2[i2] > rStop:
            break
        if i1 == len(x1) or i2 == len(x2):
            break
    return resampled


class CorbomiteGuiWidget(wx.Panel):
    def __init__(self, parent, widget):
        wx.Panel.__init__(self, parent=parent)
        self.myInitEvent, self.EVT_MY_INIT_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_MY_INIT_EVENT, self.update)
        self.widget = widget
        self.widget.addCallback(self.callbackToEventTranslator)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.yWeight = 1

    def callbackToEventTranslator(self, widget):
        evt = self.myInitEvent(attr1=widget)
        wx.PostEvent(self.GetEventHandler(), evt)

    def update(self, event):
        print "The gui widget for", self.widget.name,\
              "has no handler so event is skipped"


class CorbomiteGuiWidgetDigitalOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.box = wx.CheckBox(parent=self, label=widget.name)
        self.box.Bind(wx.EVT_CHECKBOX, self.OnClick)
        self.sizer.Add(self.box, 1, wx.GROW)

    def OnClick(self, e):
        self.widget.setValue(self.box.GetValue())

types[corbomiteWidgets.DigitalOutWidget] = CorbomiteGuiWidgetDigitalOut


class CorbomiteGuiWidgetDigitalIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.box = wx.CheckBox(parent=self, label=widget.name)
        self.box.Enable(False)
        self.sizer.Add(self.box, 1)

    def update(self, evt):
        if(evt.attr1.value > 0):
            self.box.SetValue(True)
        else:
            self.box.SetValue(False)
types[corbomiteWidgets.DigitalInWidget] = CorbomiteGuiWidgetDigitalIn


class CorbomiteGuiWidgetEventOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.button = wx.Button(parent=self,  label=self.widget.name)
        self.button.Bind(wx.EVT_BUTTON, self.onButton)
        self.sizer.Add(self.button, 1)

    def onButton(self, e):
        self.widget.setValue(None)
types[corbomiteWidgets.EventOutWidget] = CorbomiteGuiWidgetEventOut


class CorbomiteGuiWidgetAnalogOut(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.preferedPrefix, foo = \
            common.corbomiteValue.calculatePrefix(self.widget.value.getUnit())
        self.label = wx.StaticText(self, label=self.widget.name)
        self.valueText = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.valueText)
        font = wx.Font(4, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.spinX3 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinX3.SetValue(1)
        self.textX3 = wx.StaticText(self, -1, '1\n0\n0')
        self.textX3.SetFont(font)
        self.spinX2 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinX2.SetValue(1)
        self.textX2 = wx.StaticText(self, -1, '1\n0')
        self.textX2.SetFont(font)
        self.spinX1 = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinX1.SetValue(1)
        self.textX1 = wx.StaticText(self, -1, '1')
        self.textX1.SetFont(font)
        self.spinUnit = wx.SpinButton(self, style=wx.SP_VERTICAL)
        self.spinUnit.SetValue(1)
        self.textUnit = wx.StaticText(
            self, -1,
            common.corbomiteValue.prefixLetter(self.preferedPrefix))
        self.Bind(wx.EVT_SPIN, self.onPrefixSpin, self.spinUnit)
        self.Bind(wx.EVT_SPIN, self.onSpinX3, self.spinX3)
        self.Bind(wx.EVT_SPIN, self.onSpinX2, self.spinX2)
        self.Bind(wx.EVT_SPIN, self.onSpinX1, self.spinX1)
        self.slider = wx.Slider(self, wx.ID_ANY, 0, 0, 1000000)
        self.slider.Bind(wx.EVT_SCROLL, self.onSlide)
        self.updateValue(self.widget.value.minUnit)

        self.sizer.Add(self.label, 4*3)
        self.sizer.Add(self.valueText, 8*3)
        self.sizer.Add(self.textX3, 1,
                       wx.FIXED_MINSIZE, wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.spinX3, 1*3)
        self.sizer.Add(self.textX2, 1, wx.FIXED_MINSIZE)
        self.sizer.Add(self.spinX2, 1*3)
        self.sizer.Add(self.textX1, 1, wx.FIXED_MINSIZE)
        self.sizer.Add(self.spinX1, 1*3)
        self.sizer.Add(self.textUnit, 2, wx.FIXED_MINSIZE)
        self.sizer.Add(self.spinUnit, 1*3)
        self.sizer.Add(self.slider, 12*3)

    def clampValue(self, value):
        tempValue = self.widget.value
        tempValue.setUnit(value)
        tempValue.setRaw(int(tempValue.getRaw()))
        value = tempValue.getUnit()
        if value > self.widget.value.maxUnit:
            value = self.widget.value.maxUnit
        if value < self.widget.value.minUnit:
            value = self.widget.value.minUnit
        return value

    def onEnter(self, evt):
        text = self.valueText.GetValue()
        value = self.clampValue(common.corbomiteValue.stringToValue(text))
        self.updateValue(value)
        self.setSlider()

    def updateValue(self, value):
        self.shadowValue = self.clampValue(value)
        self.updateValueText()
        self.widget.setValue(value)

    def setSlider(self):
        sval = float(self.slider.GetMax()) *\
            float(self.shadowValue-self.widget.value.minUnit) /\
            float(self.widget.value.maxUnit-self.widget.value.minUnit)
        self.slider.SetValue(sval)

    def spinDelta(self, spinner):
        if spinner.GetValue() > 1:
            delta = 1
        else:
            delta = -1
        spinner.SetValue(1)
        return delta

    def onPrefixSpin(self, evt):
        self.preferedPrefix += self.spinDelta(self.spinUnit)
        self.updateValue(self.shadowValue)

    def onSpinX1(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX1)*1
        self.updateValue(self.shadowValue+d)
        self.setSlider()

    def onSpinX2(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX2)*10
        self.updateValue(self.shadowValue+d)
        self.setSlider()

    def onSpinX3(self, evt):
        d = 10**(self.preferedPrefix*3)*self.spinDelta(self.spinX3)*100
        self.updateValue(self.shadowValue+d)
        self.setSlider()

    def updateValueText(self):
        dispVal = self.shadowValue/(10**(self.preferedPrefix*3))
        dispString = str(dispVal) + ' ' +\
            common.corbomiteValue.prefixLetter(self.preferedPrefix) +\
            self.widget.value.unit
        self.valueText.SetValue(dispString)
        self.textUnit.SetLabel(
            common.corbomiteValue.prefixLetter(self.preferedPrefix))

    def onSlide(self, evt):
        self.updateValue(self.widget.value.maxUnit *
                         float(self.slider.GetValue()) /
                         float(self.slider.GetMax()))
types[corbomiteWidgets.AnalogOutWidget] = CorbomiteGuiWidgetAnalogOut


class CorbomiteGuiWidgetAnalogIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.gauge = wx.Gauge(self, wx.ID_ANY, widget.value.maxRaw -
                              widget.value.minRaw)
        self.label = wx.StaticText(self, label=self.widget.name)
        self.sizer.Add(self.label, 1)
        self.sizer.Add(self.gauge, 3)

    def update(self, event):
        self.gauge.SetValue(event.attr1.value.getRaw())
        self.label.SetLabel(self.widget.name + ' ' +
                            event.attr1.value.getValueString())
types[corbomiteWidgets.AnalogInWidget] = CorbomiteGuiWidgetAnalogIn


# This class needs some structure!
class CorbomiteGuiWidgetTraceIn(CorbomiteGuiWidget):
    def __init__(self, parent, widget):
        CorbomiteGuiWidget.__init__(self, parent, widget)
        self.rightPressed = False
        self.leftPressed = False
        self.scrolled = False
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.onRightUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.sizeEvent)
        parent.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.popupPoint = (0, 0)
        self.vMarkers = OrderedDict()
        self.hMarkers = OrderedDict()
        self.traceMemory = OrderedDict()
        self.yWeight = 10
        self.lastCoords = None
        self.pixelsPerGraticuleLine = 75
        self.autoScale()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.timer.Start(1000)
        self.time = time.time()
        self.subtract = []
        self.memorizedTraceMenu = wx.Menu()
        self.popupmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onSaveTrace, self.popupmenu.Append(-1,
                  "Save trace"))
        self.Bind(wx.EVT_MENU, self.onNewVerticalMarker, self.popupmenu.Append(
                  -1, "New vertical marker"))
        self.Bind(wx.EVT_MENU, self.onMemorizeTrace, self.popupmenu.Append(-1,
                  "Memorize trace"))
        self.Bind(wx.EVT_MENU, self.onLoadTrace,
                  self.memorizedTraceMenu.Append(-1, "Load trace"))
        self.memorizedTraceMenu.AppendSeparator()
        self.popupmenu.AppendSubMenu(self.memorizedTraceMenu,
                                     "Memorized traces")
        self.Bind(wx.EVT_MENU, self.onSubtract, self.popupmenu.Append(-1,
                  "Subtract mem"))

    def onNewVerticalMarker(self, evt):
        dlg = wx.TextEntryDialog(self, "Enter name of marker", "Enter name")
        dlg.ShowModal()
        self.vMarkers[dlg.GetValue()] = self.popupPoint[0]
        print self.vMarkers

    def onSubtract(self, evt):
        dlg = wx.SingleChoiceDialog(self, "Choose a trace to subtract from",
                                    "Subtract", list(self.traceMemory))
        dlg.ShowModal()
        v1 = dlg.GetStringSelection()
        dlg = wx.SingleChoiceDialog(self, "Choose a trace to subtract",
                                    "Subtract", list(self.traceMemory))
        dlg.ShowModal()
        v2 = dlg.GetStringSelection()
        if v1 in self.traceMemory and v2 in self.traceMemory:
            self.subtract = [v1, v2]

    def storeTraceInMem(self, trace, name):
        self.traceMemory[name] = trace
        self.memorizedTraceMenu.Append(-1, name)

    def onLoadTrace(self, event):
        fd = wx.FileDialog(self, 'Load trace', "", "",
                           'Comma separated files (*.csv)|*.csv', wx.FD_OPEN)
        fd.ShowModal()
        path = fd.GetPath()
        print "Path:", path
        with open(path, 'rb') as csvfile:
            rd = list(csv.reader(csvfile))
            x = [float(x) for x in rd[0]]
            y = [float(y) for y in rd[1]]
            dlg = wx.TextEntryDialog(self, "Enter name of trace", "Enter name",
                                     path.split('.')[0].split('/')[-1])
            dlg.ShowModal()
            self.storeTraceInMem((x, y), dlg.GetValue())

    def onMemorizeTrace(self, evt):
        dlg = wx.TextEntryDialog(self, "Enter name of trace", "Enter name")
        dlg.ShowModal()
        x = self.traceMemory[self.widget.name][0]
        y = self.traceMemory[self.widget.name][1]
        self.storeTraceInMem((x, y), dlg.GetValue())

    def onSaveTrace(self, event):
        fd = wx.FileDialog(self, 'Save trace', "", "",
                           'Comma separated files (*.csv)|*.csv', wx.FD_SAVE)
        fd.ShowModal()
        path = fd.GetPath()
        outFile = open(path, 'wb')
        wr = csv.writer(outFile)
        wr.writerow(self.traceMemory[self.widget.name][0])
        wr.writerow(self.traceMemory[self.widget.name][1])

    def onTimer(self, evt):
        if time.time() > self.time:
            self.time = time.time()
            self.rePaint()

    def update(self, evt):
        widget = evt.attr1
        if len(widget.trace) == 0:
            self.rePaint()
        self.traceMemory[widget.name] = [[], []]
        for p in widget.trace:
            trace = self.traceMemory[widget.name]
            trace[0].append(self.widget.value[0].toUnit(p[0]))
            trace[1].append(self.widget.value[1].toUnit(p[1]))
        self.time = time.time()

    def autoScale(self):
        if self.widget.name in self.traceMemory:
            self.xMin = min(self.traceMemory[self.widget.name][0])
            self.xMax = max(self.traceMemory[self.widget.name][0])
            self.yMin = min(self.traceMemory[self.widget.name][1])
            self.yMax = max(self.traceMemory[self.widget.name][1])
        else:
            self.xMin = self.yMin = 0
            self.xMax = self.yMax = 1

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
            self.xMax += dx
            self.yMax += dy
            self.xMin += dx
            self.yMin += dy
            self.rePaint()
            self.lastCoords = (evt.GetX(), evt.GetY())

    def onLeftUp(self, evt):
        self.leftPressed = False
        self.lastCoords = None

    def onDoubleClick(self, evt):
        self.autoScale()
        self.rePaint()

    def onRightDown(self, evt):
        self.rightPressed = True

    def onRightUp(self, evt):
        self.rightPressed = False
        if not self.scrolled:
            pos = evt.GetPosition()
            self.popupPoint = pos
            self.PopupMenu(self.popupmenu, pos)
        self.scrolled = False

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
        self.scrolled = True
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
            tens += 1

    def getGraticuleResolution(self, axisRange, axisSize):
        maxGraticuleLines = axisSize/self.pixelsPerGraticuleLine
        firstGuess = axisRange/maxGraticuleLines
        return self.findClosest125(firstGuess)

    def xAxisToPixels(self, x):
        (winx, winy) = self.GetSize()
        pixelsPerUnit = winx/(self.xMax-self.xMin)
        xPixels = (x - self.xMin)*pixelsPerUnit
        return max(min(xPixels, winx+1), -1)

    def yAxisToPixels(self, y):
        (winx, winy) = self.GetSize()
        pixelsPerUnit = winy/(self.yMax - self.yMin)
        yPixels = winy-(y-self.yMin)*pixelsPerUnit
        return max(min(yPixels, winy+1), -1)

    def computeScale(self, axisMax, axisMin, axisLengthInPixels):
        axisMax = float(axisMax)
        axisMin = float(axisMin)
        axisRange = axisMax - axisMin
        if axisRange < 1e-18:
                axisRange = 1
        graticuleResolution = self.getGraticuleResolution(axisRange,
                                                          axisLengthInPixels)
        startGraticule = axisMin - axisMin % graticuleResolution
        currentGraticule = startGraticule
        gls = []  # Graticule lines as pixel coordinates
        while True:
            gls.append(currentGraticule)
            currentGraticule += graticuleResolution
            if currentGraticule > axisMax:
                break
        return (gls, graticuleResolution)

    def drawScale(self, dc):
        (winx, winy) = self.GetSize()
        (glsY, ry) = self.computeScale(self.yMax, self.yMin, winy)
        (glsX, rx) = self.computeScale(self.xMax, self.xMin, winx)
        dc.SetPen(wx.Pen("GREY", 3))
        first = True
        for ya in glsY[1:]:
            y = self.yAxisToPixels(ya)
            dc.DrawLine(0, y, winx, y)
            if first:
                yString = self.widget.value[1].getPrecisionString(ya, 2) + "\n"\
                    + self.widget.value[1].getPrecisionString(ry, 2) + "/div"
                dc.DrawText(yString,
                            0, y-36)
                dc.SetPen(wx.Pen("GREY", 1))
                first = False

        dc.SetPen(wx.Pen("GREY", 3))
        first = True
        for xa in glsX[1:]:
            x = self.xAxisToPixels(xa)
            dc.DrawLine(x, 0, x, winy)
            if first:
                xString = self.widget.value[0].getPrecisionString(xa, 2) + "\n"\
                    + self.widget.value[0].getPrecisionString(rx, 2) + "/div"
                dc.DrawText(xString,
                            x, 0)
                dc.SetPen(wx.Pen("GREY", 1))
                first = False

    def drawPlot(self, dc, name, points):
        (winx, winy) = self.GetSize()
        if self.xMax != self.xMin:
            xpixelsPerUnit = winx/(self.xMax-self.xMin)
            ypixelsPerUnit = winy/(self.yMax-self.yMin)
        else:
            xpixelsPerUnit = winx
            ypixelsPerUnit = winy
        for i in range(len(points)-1):
            p1 = points[i]
            p2 = points[i+1]
            x1 = min((p1[0]-self.xMin)*xpixelsPerUnit, winx+1)
            y1 = min(winy-(p1[1]-self.yMin)*ypixelsPerUnit, winy+1)
            x2 = min((p2[0]-self.xMin)*xpixelsPerUnit, winx+1)
            y2 = min(winy-(p2[1]-self.yMin)*ypixelsPerUnit, winy+1)
            dc.DrawLine(x1, y1, x2, y2)

    def render(self, dc):
        c = wx.Colour(200, 200, 200)
        brush = wx.Brush(c, wx.SOLID)
        dc.SetBackground(brush)
        dc.Clear()
        self.drawScale(dc)
        clist = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE',
                 'VIOLET', 'GREY', 'WHITE']
        i = 0
        (w, h) = self.GetSize()
        for name in self.traceMemory:
            c = wx.NamedColour(clist[i % len(clist)])
            dc.SetPen(wx.Pen(c))
            points = zip(self.traceMemory[name][0], self.traceMemory[name][1])
            self.drawPlot(dc, name, points)
            dc.SetTextForeground(c)
            dc.DrawText(name, w-100, i*15+15)
            i += 1
            # if i >= len(clist):
            #    i = 0
        if len(self.subtract) == 2:
            resampled1 = resample(self.traceMemory[self.subtract[0]],
                                  self.traceMemory[self.subtract[1]][0])
            resampled2 = resample(self.traceMemory[self.subtract[1]],
                                  self.traceMemory[self.subtract[0]][0])

            for j in range(len(resampled1[0])):
                resampled1[1][j] -= resampled2[1][j]
            points = zip(resampled1[0], resampled1[1])
            c = wx.NamedColour("MAGENTA")
            dc.SetPen(wx.Pen(c))
            dc.SetTextForeground(c)
            self.drawPlot(dc, "subtract", points)
            dc.DrawText("subtract", w-100, i*15+15)

        c = wx.NamedColour("GREEN")
        dc.SetPen(wx.Pen(c))
        for m in self.vMarkers:
            dc.DrawLine(self.vMarkers[m], 0, self.vMarkers[m], h)


types[corbomiteWidgets.TraceInWidget] = CorbomiteGuiWidgetTraceIn


def createWidget(parent, widget):
    try:
        constr = types[widget.__class__]
        return constr(parent, widget)
    except KeyError:
        print "WARNING", widget.__class__, "is not supported"
