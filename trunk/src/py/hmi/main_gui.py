import wx
import wx.aui
import deviceManagerPanel
import openDeviceDialog
import corbomiteDevice
import devicePanel
import serial
import sys
class RootFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Corbomite",
                          size=(600,800))
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
			    self.openPort(serial.Serial(p, 9600, timeout = 1))
        #self.openPort(serial.Serial('/dev/ttyUSB0', 9600, timeout = 1))


    def onOpenDevice(self, event):
        self.openDlg = openDeviceDialog.OpenDeviceDialog()
        if self.openDlg.ShowModal() == wx.ID_OK:
            self.openPort(self.openDlg.port)
        
    def openPort(self, port):
        dp = devicePanel.DevicePanel(self.deviceManager.nb)
        corbomiteDevice.CorbomiteDevice(port, [dp.receiveCallback], initCallbacks = [dp.initCallback])
        self.deviceManager.addPage(dp, port.port)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = RootFrame()
    app.MainLoop()
