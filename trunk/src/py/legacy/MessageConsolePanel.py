__author__ = "bjohan"

import sys
import wx
import wx.aui


class MessageConsolePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(-1, 200))
        self.sizer = wx.GridSizer(1, 1)
        self.console = wx.TextCtrl(self, -1, '',
                                   style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.sizer.Add(self.console, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        sys.stdout = self

    def write(self, string):
        self.console.AppendText(string)
