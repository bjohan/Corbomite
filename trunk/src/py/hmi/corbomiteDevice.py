import serial
import threading
import thread
import time
import corbomiteWidgets
import com.corbomiteIo
class CorbomiteDevice(com.corbomiteIo.CorbomiteIo):
    def __init__(self, io, frameCallbacks = [], initCallbacks = [], eventCallbacks = []):
	com.corbomiteIo.CorbomiteIo.__init__(self, io, frameCallbacks, initCallbacks, eventCallbacks)
	self.widgets = {}
        print "Sending info"
        self.writer.write("info");
        print "Waiting for data..."
        while self.busy:
            pass
        print "Done!!"
        print "registered widgets:",
        for key in self.widgets:
            print key,
        print

    def __del__(self):
        print "Del for corbomitedevice called"
        self.reader.stop()
        self.writer.stop()

    def frameReceiver(self, frame):
        #print "Got %d bytes in frame:"%(len(frame)), frame
        if frame == 'busy':
            self.busy = True
        elif frame == 'idle':
            print "Idle"
            self.init = False
            self.busy = False
        elif self.init:
            w = corbomiteWidgets.CorbomiteWidget.factory(frame, self)
	    for i in self.initCallbacks:
		i(w)
        else:
            name = frame.split()[0]
            if name in self.widgets:
                self.widgets[name].process(frame)
            else:
                print "WARNING: name in frame is not registered", frame

    def write(self, data):
        print "Writing" , data, "to device"
        self.writer.write(data)
