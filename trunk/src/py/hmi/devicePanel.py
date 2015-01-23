import wx
import wx.aui
import corbomiteGuiWidgetFactory
import wx.lib.newevent


class DevicePanel(wx.Panel):
    def __init__(self, parent):
        print "Device panel constructor start"
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.widgets = {}
        self.parent = parent
        self.myInitEvent, self.EVT_MY_INIT_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_MY_INIT_EVENT, self.receiveInitEvent)
        self.parent.Layout()
        print "Device panel constructor finished"

    def receiveInitEvent(self, widget):
        new = corbomiteGuiWidgetFactory.createWidget(self, widget)
        if new is not None:
            self.sizer.Add(new, new.yWeight, wx.EXPAND)
            self.sizer.Layout()

    def initCallback(self, widget):
        wx.CallAfter(self.receiveInitEvent, widget)

    def receiveCallback(self, data):
        pass
