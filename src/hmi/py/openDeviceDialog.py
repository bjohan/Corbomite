import wx
import serial
import serial.tools.list_ports
import corbomiteDevice
import serial

class OpenDeviceDialog(wx.Dialog):
    def __init__(self):
        self.corbomiteDevice = None
        wx.Dialog.__init__(self, None, wx.ID_ANY, 'Open device')
        self.panel = wx.Panel(self)
        self.vertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Serial port widgets
        self.serialSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.serialText = wx.StaticText(self.panel, wx.ID_ANY, 'Serial Device:')
        self.serialCombo = wx.ComboBox(self.panel, choices = self.getSerialPortList())

        self.openSerialButton = wx.Button(self.panel, wx.ID_ANY, 'Open')
        self.openSerialButton.Bind(wx.EVT_BUTTON, self.onOpen)

        self.vertSizer.Add(self.serialText, 0, wx.ALL)
        self.serialSizer.Add(self.serialCombo, 0, wx.ALL)
        self.serialSizer.Add(self.openSerialButton, 0, wx.ALL)
        self.vertSizer.Add(self.serialSizer, 0, wx.ALL)

        #Add open file button
        self.openSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fileText = wx.StaticText(self.panel, wx.ID_ANY, 'File device:')
        self.vertSizer.Add(self.fileText, 0, wx.ALL)
        self.openFileDevButton = wx.Button(self.panel, wx.ID_ANY, "Open file device")
        self.openProcDevButton = wx.Button(self.panel, wx.ID_ANY, "Open process device")
        self.openSizer.Add(self.openFileDevButton, 0, wx.ALL)
        self.openSizer.Add(self.openProcDevButton, 0, wx.ALL)
        self.vertSizer.Add(self.openSizer, 0, wx.ALL)
 
        self.panel.SetSizer(self.vertSizer)
        self.vertSizer.Fit(self)

        self.getSerialPortList()

    def onOpen(self, fooEvent):
        print "Opening", self.serialCombo.GetValue()
        self.port = serial.Serial(self.serialCombo.GetValue(), 9600, timeout = 1)
        #self.corbomiteDevice = corbomiteDevice.CorbomiteDevice(port)
        self.EndModal(wx.ID_OK)
    

    def getSerialPortList(self):
        ports = list(serial.tools.list_ports.comports())
        devs = []
        for p in reversed(ports):
            devs.append(p[0])
        return devs
