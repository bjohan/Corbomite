import wx
import wx.aui
import deviceManagerPanel
import openDeviceDialog
from client import corbomiteClient
import devicePanel
import serial
import sys
from common.tcpCommunication import TcpClient


class RootFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Corbomite",
                          size=(600, 800))
        self.icon = wx.Icon('corbomite.png', wx.BITMAP_TYPE_ANY)
        wx.Frame.SetIcon(self, self.icon)
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menuBar.Append(menu, "&File")
        self.openDeviceId = wx.NewId()
        menu.Append(self.openDeviceId, "Open Corbomite Device")
        wx.EVT_MENU(self, self.openDeviceId, self.onOpenDevice)
        self.SetMenuBar(menuBar)
        self.deviceManager = deviceManagerPanel.DeviceManagerPanel(self)
        self.Show()
        if len(sys.argv) > 1:
            for p in sys.argv[1:]:
                t = p.split(':')
                if t[0].upper() == 'SERIAL':
                    baud = 9600
                    if len(t) > 2:
                        baud = int(t[2])
                    self.openPort(serial.Serial(t[1], baud, timeout=1))
                else:
                    self.openPort(TcpClient(t[1]))

    def onOpenDevice(self, event):
        self.openDlg = openDeviceDialog.OpenDeviceDialog()
        if self.openDlg.ShowModal() == wx.ID_OK:
            self.openPort(self.openDlg.port)

    def openPort(self, port):
        dp = devicePanel.DevicePanel(self.deviceManager.nb)
        corbomiteClient.CorbomiteClient(port, [dp.receiveCallback],
                                        initCallbacks=[dp.initCallback])
        self.deviceManager.addPage(dp, port.port)


def run():
    app = wx.PySimpleApp()
    frame = RootFrame()
    frame.Show()
    app.MainLoop()
