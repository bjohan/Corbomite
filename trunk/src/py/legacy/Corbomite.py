#!/usr/bin/python
__author__="bjohan"

import sys
import wx
import wx.aui
from MessageConsolePanel import *
from InterfacePanel import *
from PlotPanel import *
from SignalPanel import *
class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Corbomite', size=(800,600), 
								pos = (0,0))
        self.menuBar = wx.MenuBar()
        self.file = wx.Menu()
        self.operations = wx.Menu()
        self.saveId = wx.NewId()
        self.file.Append(self.saveId, '&Save', 'Save settings')
        self.loadId = wx.NewId()
        self.file.Append(102, '&Load', 'Load settings')
        self.exitId = wx.NewId()
        self.file.Append(103, '&Exit', 'Exit Corbomite')

        self.newIoInterfaceId = wx.NewId()
        self.operations.Append(self.newIoInterfaceId, 'New &IO interface')
        self.Bind(wx.EVT_MENU, self.onNewIoInterface, id=self.newIoInterfaceId)
        self.ioInterfacesTabPanel = IoInterfacesTabPanel(self)

        self.newDataSourceId = wx.NewId()
        self.operations.Append(105, 'New &signal')

      	self.newPlotId = wx.NewId()
        self.operations.Append(self.newPlotId, 'New plot')
        self.Bind(wx.EVT_MENU, self.onNewPlot, id=self.newPlotId)

        self.menuBar.Append(self.file, '&File')
        self.menuBar.Append(self.operations, '&Operations')

        self.SetMenuBar(self.menuBar)

        self.messageConsole = MessageConsolePanel(self)
	
        self.mgr = wx.aui.AuiManager(self)
	
        self.plotPanel = PlotPanel(self)
        self.mgr.AddPane(self.plotPanel, wx.CENTER, 'Plots')

        self.signalPanel = SignalPanel(self)	
        self.mgr.AddPane(self.signalPanel, wx.TOP, 'Signal manager')
        self.mgr.AddPane(self.ioInterfacesTabPanel, wx.RIGHT,'Input devices')
        self.mgr.AddPane(self.messageConsole, wx.BOTTOM,'Message console')

        self.mgr.Update()
        self.Show(True)
        self.messageConsole.write("Welcome!")
        
    def onNewIoInterface(self, event):
        self.ioInterfacesTabPanel.addInterface()

    def onNewPlot(self, event):
		self.plotPanel.addPlot()
app = wx.App()
MainWindow()
app.MainLoop()

