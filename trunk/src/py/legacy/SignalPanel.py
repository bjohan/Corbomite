__author__ = "bjohan"

import sys
import wx
import wx.aui
import SignalPlotterPanel


class SignalPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(-1, 200))
        self.sizer = wx.GridSizer(1, 1)
        self.text = wx.StaticText(self, -1, 'Signal manager')
        self.sizer.Add(self.text, 1, wx.EXPAND)
        #self.plotter = SignalPlotterPanel.SignalPlotterPanel(self)
        #self.sizer.Add(self.plotter, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
