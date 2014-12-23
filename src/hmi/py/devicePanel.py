import wx
import wx.aui
import corbomiteGuiWidgetFactory

class DevicePanel(wx.Panel):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.widgets = {} 

    def initCallback(self, widget):
        new = corbomiteGuiWidgetFactory.createWidget(self, widget);
        if new is not None: 
            print new.yWeight
            self.sizer.Add(new, new.yWeight, wx.GROW)
            self.SetSizerAndFit(self.sizer)
            self.Show()

    def receiveCallback(self, data):
        pass
