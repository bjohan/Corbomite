__author__="bjohan"

import sys
import wx
import wx.aui
import InterfaceHandler

class IoInterfaceSettingsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
	self.resetButtonId = wx.NewId()
        self.resetButton = wx.Button(self, self.resetButtonId,"Reset interface")
	self.startButtonId = wx.NewId()
	self.startButton = wx.Button(self, self.startButtonId, "Start")
	self.stopButtonId = wx.NewId()
	self.stopButton = wx.Button(self, self.stopButtonId, "Stop")
	self.cmdText = wx.TextCtrl(self, -1, 
		'./TestSource.py --time-stamp --sin 3 --rate 10000', 
		style = wx.TE_MULTILINE)
	sizer = wx.GridSizer(4,1)
	sizer.Add(self.cmdText, 1,wx.EXPAND)
	sizer.Add(self.resetButton,0, wx.EXPAND )
	sizer.Add(self.startButton,0, wx.EXPAND)
	sizer.Add(self.stopButton,0, wx.EXPAND)
	self.SetSizer(sizer)
	self.Fit()
	self.Bind(wx.EVT_BUTTON, self.onResetButton, id = self.resetButtonId)
	self.Bind(wx.EVT_BUTTON, self.onStartButton, id = self.startButtonId)
	self.Bind(wx.EVT_BUTTON, self.onStopButton, id = self.stopButtonId)
	self.ih = InterfaceHandler.InterfaceHandler()

    def onResetButton(self, event):
	print "Resetting interface"
	if self.ih.running:
		self.onStopButton(event)
	self.onStartButton(event)

    def onStartButton(self, event):
	print "Starting interface:", self.cmdText.GetValue()
	self.ih = None
	self.ih = InterfaceHandler.InterfaceHandler()
	self.ih.setCommand(self.cmdText.GetValue())
	self.ih.start()

    def onStopButton(self, event):
	self.ih.stop()
	print "Stopping interface"

class IoInterfacesTabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size = (200,-1))

        self.nb = wx.aui.AuiNotebook(self)

        self.interfaces = []
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def addInterface(self):
        self.interfaces.append(IoInterfaceSettingsPanel(self))
        self.nb.AddPage(self.interfaces[-1],
					'Interface '+str(len(self.interfaces)))

