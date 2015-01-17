import ThreadedSerialPort
import thread
import random
import time


class IbasicInterface():

    def __init__(self):
        self.serialPort = ThreadedSerialPort.ThreadedSerialPort()
        self.serialPort.start()
        self.lock = thread.allocate_lock()

    def __del__(self):
        print "Stopping serial thread"
        self.serialPort.stop()

    def SendProgram(self, text):
        self.lock.acquire()
        self.serialPort.readData()
        self.serialPort.sendData('scratch\n')
        lines = text.splitlines()
        lnum = 10
        endLine = ''
        for line in lines:
            if line[-1] != '\n':
                line += '\n'
            self.serialPort.sendData("%d " % (lnum) + line)
            lnum += 10
        if not 'end' in lines[-1]:
            endLine = "%d end\n" % (lnum)
            self.serialPort.sendData(endLine)
        self.lock.release()
        self.serialPort.readData()
        self.FindOutputSequence([endLine[:-1]], maxTime=20)
        return endLine

    def FindOutputSequence(self, sequence, maxTime=10):
        # print "Locking"
        self.lock.acquire()
        # print "Looking"
        data = ''
        dc = ''
        fragments = []
        t0 = time.time()
        for s in sequence:
            print "Looking for", s
            while True:
                # print "looking for", s

                incr = ''.join(self.serialPort.readData())
                data += incr
                dc += incr
                # if incr != '':
                #	print "data:", data
                if s in data:
                    p = data.find(s) + len(s)
                    # print "fragment:", data[offset:p]
                    fragments.append(data[:p])
                    data = data[p:]
                    t0 = time.time()
                    break
                if time.time() > t0 + maxTime:
                    print "Timeout:", s
                    print "Data was:", data
                    print "Complete data:", dc
                    break
        self.lock.release()
        print "Complete data:", dc
        return fragments

    def RunProgram(self):
        self.lock.acquire()
        self.serialPort.readData()
        self.serialPort.sendData('run\n')
        self.lock.release()
        self.FindOutputSequence(['run'])

    def SendProgramGetOutput(self, text, timeout=5):
        randString = ''
        for i in range(10):
            randString += chr(ord('A') + int(25 * random.random()))
        text += 'print "' + (randString) + '"' + '\n'
        # print "Text is:", text
        endLine = self.SendProgram(text)
        endLine = endLine[:-1]
        # print "end of program is:", endLine
        lastTime = time.time()
        data = ''
        while True:
            got = ''.join(self.serialPort.readData())
            if got != '':
                lastTime = time.time()
                data += got
                if data.count(randString) > 1:
                    # print "occur", data.count(randString)
                    # print "COMPLETE DATA----",data
                    # print "======================="
                    start = data.find(endLine)
                    # print "start pos", start
                    if start == -1:
                        start = 0
                    else:
                        start += len(endLine)
                    data = data[start:]
                    end = data.find(randString)
                    return data[:end]
                if time.time() > lastTime + timeout:
                    return 'TIMEOUT'

    def SendInput(self, data):
        self.lock.acquire()
        self.serialPort.sendData(data)
        self.lock.release()

    def GetOutput(self):
        self.lock.acquire()
        d = self.serialPort.readData()
        self.lock.release()
        return d
