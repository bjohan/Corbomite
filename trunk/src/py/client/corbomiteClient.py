import corbomiteWidgets
import common.corbomiteIo
import time
from collections import OrderedDict


class CorbomiteClient(common.corbomiteIo.CorbomiteIo):
    def __init__(self, io, frameCallbacks=[], initCallbacks=[],
                 eventCallbacks=[]):
        common.corbomiteIo.CorbomiteIo.__init__(self, io, frameCallbacks,
                                                initCallbacks, eventCallbacks)
        self.writeQueue = {}
        self.widgets = OrderedDict()
        print "Sending info"
	time.sleep(2);
        self.writer.write("info")
        t0= time.time();
        #time.sleep(1)
        print "Waiting for data..."
        while self.busy:
            if time.time()-t0 > 10:
                print "No response after 10 seconds, resending info"
                self.writer.write("info");
                t0=time.time()
                time.sleep(0.1)
        
        print "Done!!"
        print "registered widgets:",
        for key in self.widgets:
            print key,
        print

    def __del__(self):
        common.corbomiteIo.CorbomiteIo.__del__(self)
        print "Del for corbomitedevice called"
        self.reader.stop()
        self.writer.stop()

    def frameReceiver(self, frame):
        #print "Got %d bytes in frame:" % (len(frame)), frame
        if frame == 'busy':
            #print "<BUSY>"
            self.busy = True
        elif frame == 'idle':
            if len(self.writeQueue):
                xmitKey = self.writeQueue.keys()[0]
                # print "transmitting buffered", self.writeQueue[xmitKey]
                self.writer.write(self.writeQueue[xmitKey])
                del self.writeQueue[xmitKey]
            else:
                # print "Idle"
                self.busy = False
                #print "<IDLE>"
        elif frame.split()[0] == "info":
            w = corbomiteWidgets.CorbomiteWidget.factory(frame[4:], self)
            for i in self.initCallbacks:
                i(w)
        else:
            name = frame.split()[0]
            if name in self.widgets:
                self.widgets[name].process(frame)
            else:
                print "WARNING: name in frame is not registered", frame

    def write(self, writer, data):
        if self.busy:
             #print "Busy, buffering", data
             self.writeQueue[writer] = data
        else:
            self.busy = True
            #print "<BUSY local>", data
            self.writer.write(data)
            while self.busy:
                pass
