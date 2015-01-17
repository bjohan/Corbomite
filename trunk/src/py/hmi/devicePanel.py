import wx
import wx.aui
import corbomiteGuiWidgetFactory
import wx.lib.newevent


class DevicePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.widgets = {}
        self.parent = parent
        self.myInitEvent, self.EVT_MY_INIT_EVENT = wx.lib.newevent.NewEvent()
        self.Bind(self.EVT_MY_INIT_EVENT, self.receiveInitEvent)
        self.parent.Layout()

    def receiveInitEvent(self, evt):
        widget = evt.attr1
        new = corbomiteGuiWidgetFactory.createWidget(self, widget)
        if new is not None:
            self.sizer.Add(new, new.yWeight, wx.EXPAND)
            self.sizer.Layout()

    def initCallback(self, widget):
        evt = self.myInitEvent(attr1=widget)
        wx.PostEvent(self.GetEventHandler(), evt)
        pass

    def receiveCallback(self, data):
        pass
