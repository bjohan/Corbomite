import wx
import serial
import serial.tools.list_ports
import serial
import common.tcpCommunication


class OpenDeviceDialog(wx.Dialog):
    def __init__(self):
        self.corbomiteDevice = None
        wx.Dialog.__init__(self, None, wx.ID_ANY, 'Open device', size =(600, 100))
        self.panel = wx.Panel(self)
        self.vertSizer = wx.BoxSizer(wx.VERTICAL)

        # Serial port widgets
        self.serialSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.serialText = wx.StaticText(self.panel, wx.ID_ANY,
                                        'Serial Device:')
        ports = self.getSerialPortList()
        self.serialCombo = wx.ComboBox(self.panel, value=ports[0],
                                       choices=ports)
        self.baudRatecombo = wx.ComboBox(self.panel, value="9600",
                                         choices=["300", "1200", "2400",
                                                  "4800", "9600", "14400",
                                                  "19200", "28800", "38400",
                                                  "57600", "115200", "230400",
                                                  "460800", "921600"])
        self.openSerialButton = wx.Button(self.panel, wx.ID_ANY, 'Open serial')
        self.openSerialButton.Bind(wx.EVT_BUTTON, self.onOpenSerial)

        self.vertSizer.Add(self.serialText, 0, wx.ALL)
        self.serialSizer.Add(self.serialCombo, 0, wx.ALL)
        self.serialSizer.Add(self.baudRatecombo, 0, wx.ALL)
        self.serialSizer.Add(self.openSerialButton, 0, wx.ALL)
        self.vertSizer.Add(self.serialSizer, 0, wx.ALL)

        # Bluetooth widgets
        self.bluetoothSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bluetoothLabel = wx.StaticText(self.panel, wx.ID_ANY,
                                      'Bluetooth device:')
        self.bluetoothText = wx.TextCtrl(self.panel, value='00:00:00:00:00:00')

        self.openBluetoothButton = wx.Button(self.panel, wx.ID_ANY, 'Open bluetooth')
        self.openBluetoothButton.Bind(wx.EVT_BUTTON, self.onOpenBluetooth)

        self.vertSizer.Add(self.bluetoothLabel, 2, wx.ALL)
        self.bluetoothSizer.Add(self.bluetoothText, 3, wx.ALL)
        self.bluetoothSizer.Add(self.openBluetoothButton, 2, wx.ALL)
        self.vertSizer.Add(self.bluetoothSizer, 0, wx.ALL)

        # TCP widgets
        self.tcpSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tcpLabel = wx.StaticText(self.panel, wx.ID_ANY,
                                      'TCP Device:')
        self.tcpText = wx.TextCtrl(self.panel, value='127.0.0.1')

        self.openTcpButton = wx.Button(self.panel, wx.ID_ANY, 'Open tcp')
        self.openTcpButton.Bind(wx.EVT_BUTTON, self.onOpenTcp)

        self.vertSizer.Add(self.tcpLabel, 0, wx.ALL)
        self.tcpSizer.Add(self.tcpText, 0, wx.ALL)
        self.tcpSizer.Add(self.openTcpButton, 0, wx.ALL)
        self.vertSizer.Add(self.tcpSizer, 0, wx.ALL)

        # Add open file button
        self.openSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fileText = wx.StaticText(self.panel, wx.ID_ANY, 'File device:')
        self.vertSizer.Add(self.fileText, 0, wx.ALL)
        self.openFileDevButton = wx.Button(self.panel, wx.ID_ANY,
                                           "Open file device")
        self.openProcDevButton = wx.Button(self.panel, wx.ID_ANY,
                                           "Open process device")
        self.openSizer.Add(self.openFileDevButton, 0, wx.ALL)
        self.openSizer.Add(self.openProcDevButton, 0, wx.ALL)
        self.vertSizer.Add(self.openSizer, 0, wx.ALL)

        self.panel.SetSizer(self.vertSizer)
        self.vertSizer.Fit(self)
	self.panel.Fit()
        self.getSerialPortList()
	self.Fit()

    def onOpenBluetooth(self, fooEvent):
	addr = self.bluetoothText.GetValue()
	print "Opening", addr
	from common.bluetoothIo import BluetoothIo
	self.port = BluetoothIo(addr)
	self.EndModal(wx.ID_OK)

    def onOpenTcp(self, fooEvent):
        addr = self.tcpText.GetValue()
        print "Opening", addr
        self.port = common.tcpCommunication.TcpClient(addr, 8472)
        self.EndModal(wx.ID_OK)

    def onOpenSerial(self, fooEvent):
        print "Opening", self.serialCombo.GetValue()
        self.port = serial.Serial(self.serialCombo.GetValue(),
                                  int(self.baudRatecombo.GetValue()),
                                  timeout=1)
        self.EndModal(wx.ID_OK)

    def getSerialPortList(self):
        ports = list(serial.tools.list_ports.comports())
        devs = []
        for p in reversed(ports):
            devs.append(p[0])
        return devs
