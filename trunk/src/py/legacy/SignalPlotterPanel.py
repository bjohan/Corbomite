import wx
import wx.aui
import SignalSocket
from wxPython.glcanvas import wxGLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *


class PlotterContextMenu(wx.Menu):

    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.name = wx.MenuItem(self, wx.NewId(), parent.name)
        self.addSignalId = wx.NewId()
        self.addSignal = wx.MenuItem(self, self.addSignalId,
                                     "Add signal")
        self.AppendItem(self.name)
        self.AppendItem(self.addSignal)
        self.Bind(wx.EVT_MENU, parent.OnAddSignal)


class SignalPlotterPanel(wxGLCanvas):

    def __init__(self, parent, name):
        wxGLCanvas.__init__(self, parent, -1)
        wx.EVT_PAINT(self, self.OnPaint)
        self.init = 0
        self.name = name
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        print "plot panel", self.name
        print "Size", self.GetSize()
        (width, height) = self.GetSize()
        height = max(1, height)
        rat = float(width) / float(height)
        glViewport(0, 0, width, height)
        # glMatrixMode(GL_ORTHO)
        glLoadIdentity()
        print rat
        gluPerspective(90.0, rat, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def OnRightDown(self, event):
        self.PopupMenu(PlotterContextMenu(self), event.GetPosition())

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = 1
        self.OnDraw()
        return

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        color = [1.0, 0.0, 0.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glutSolidSphere(2, 20, 20)
        glPopMatrix()
        self.SwapBuffers()

    def InitGL(self):
        glutInit()
        glClearColor(0, 0, 0, 1.0)
        glClearDepth(1.0)
        self.OnSize(None)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        #gluPerspective(40, 1.0, 1.0, 30.0)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()
        glLoadIdentity()
        glTranslate(0.0, 0.0, -10)
        #gluLookAt(0.0, 0.0, 10.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)
        return

    def OnAddSignal(self, event):
        print "Adding signal for", self.name
