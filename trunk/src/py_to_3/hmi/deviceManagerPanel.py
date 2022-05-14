import wx
import wx.aui


class DeviceManagerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.nb = wx.aui.AuiNotebook(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def addPage(self, dev, name):
        self.nb.AddPage(dev, name)
