import threading
import popen2
import copy


class InterfaceHandler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.commandString = ''
        self.signalSocket = None
        self.running = True

    def setCommand(self, c):
        self.commandString = copy.deepcopy(str(c))
        print "Hello", self.commandString

    def setSignalSocket(self, socket):
        self.signalSocket = socket

    def run(self):
        # print "executing", self.commandString
        (self.fin, self.fout) = popen2.popen2(self.commandString)
        # return
        while self.running:
            s = self.fin.readline()
            for word in s.split(','):
                try:
                    v = float(word)
                except:
                    pass
                else:
                    with self.signalSocket:
                        self.signalSocket.AddSample(v)
                    # signalValues.append(v)
                    # use signal socket here later
            # print signalValues

    def stop(self):
        self.running = False
        self.fout.write('exit\n')
        self.fout.flush()
        # TODO kill process properly


# ih = InterfaceHandler()
# ih.setCommand('python TestSource.py --time-stamp --sin 3 --rate 10000')
# ih.start()
# time.sleep(5)
# ih.stop()
