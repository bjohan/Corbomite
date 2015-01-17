__author__ = "bjohan"

import sys
import wx
import wx.aui
import SignalPlotterPanel


class PlotPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, size=(-1, 200))
        self.nb = wx.aui.AuiNotebook(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.signalPlotPanels = []

    def addPlot(self):
        print "Adding plot"
        dlg = wx.TextEntryDialog(self, 'Name:', 'Enter name of plot',
                                 'plot' + str(len(self.signalPlotPanels)))
        dlg.ShowModal()
        self.signalPlotPanels.append(
            SignalPlotterPanel.SignalPlotterPanel(self, dlg.GetValue()))
        self.nb.AddPage(self.signalPlotPanels[-1], dlg.GetValue())
