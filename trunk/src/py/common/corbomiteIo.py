import threading


class FrameInfo:
    def __init__(self):
        self.fs = "#"
        self.fe = "\r\n"
        self.esc = "\\"


class FrameDecoder(FrameInfo):
    def __init__(self):
        FrameInfo.__init__(self)
        self.buf = ''

    def addData(self, data):
        self.buf += data

    def strFindEscaped(self, haystack, needle, esc):
        nl = len(needle)
        escaped = False
        match = 0
        idx = 0
        for c in haystack:
            if c == esc and not escaped:
                escaped = True
            else:
                if not escaped:
                    if c == needle[match]:
                        match += 1
                    else:
                        match = 0
                    if match == nl:
                        return idx
                escaped = False
            idx += 1
        return -1

    def getFrameIndexes(self):
        frameStart = self.strFindEscaped(self.buf, self.fs, self.esc)
        # print "frameStart", frameStart
        if frameStart >= 0:
            frameEnd = self.strFindEscaped(self.buf, self.fe, self.esc)
            # print "frameEnd", frameEnd
            if frameEnd >= 0:
                return (frameStart, frameEnd)
        return None

    def getFrame(self):
        i = self.getFrameIndexes()
        if i is None:
            return None

        if i[0] < i[1]:
            d = self.buf[i[0]+len(self.fs):i[1]-1]
            self.buf = self.buf[i[1]+1:]
            return d

        self.buf = self.buf[i[1]:]
        return None

    def getAllFrames(self):
        frames = []
        while True:
            frame = self.getFrame()
            # print "Parsed frame", frame
            if frame is None:
                break
            frames.append(frame)
        return frames


class FrameEncoder(FrameInfo):
    def __init__(self):
        FrameInfo.__init__(self)
        self.encoded = ''

    def encodeData(self, data):
        self.encoded += self.fs
        for d in data:
            if d in (self.fe, self.fs, self.esc):
                self.encoded += self.esc
            self.encoded += d
        self.encoded += self.fe

    def getEncodedData(self):
        d = self.encoded
        self.encoded = ''
        return d


class CorbomiteWriteThread(threading.Thread):
    def __init__(self, io, callbacks):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.callbacks = callbacks
        self.fe = FrameEncoder()
        self.o = io
        self.m = threading.Lock()
        self.s = threading.Semaphore()
        self.doExit = False
        self.start()

    def run(self):
        while True:
            self.s.acquire()
            if self.doExit:
                break
            self.m.acquire()
            data = self.fe.getEncodedData()
            self.o.write(data)
            self.m.release()
        print "Writeloop exited"
        self.join()

    def write(self, data):
        self.m.acquire()
        self.fe.encodeData(data)
        self.m.release()
        self.s.release()

    def stop(self):
        self.m.acquire()
        self.doExit = True
        self.m.release()
        self.s.release()

    def __del__(self):
        print "del for writer called"
        self.stop()


class CorbomiteReadThread(threading.Thread):
    def __init__(self, io, callbacks):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.i = io
        self.m = threading.Lock()
        self.s = threading.Semaphore()
        self.callbacks = callbacks
        self.fd = FrameDecoder()
        self.exit = False
        self.start()

    def addCallback(self, cbk):
        self.callbacks.append(cbk)

    def run(self):
        while True:
            self.m.acquire()
            if self.exit:
                break
            d = self.i.read()
            if len(d) > 0:
                self.fd.addData(d)
                for frame in self.fd.getAllFrames():
                    for callback in self.callbacks:
                        callback(frame)
            self.m.release()
            self.s.release()
        print "Readloop exited"
        self.join()

    def read(self):
        self.s.acquire()
        self.m.acquire()
        data = self.data
        self.data = ''
        self.m.release()
        return data

    def stop(self):
        self.m.acquire()
        self.exit = True
        self.m.release()

    def __del__(self):
        print "del for reader called"
        self.stop()


class CorbomiteIo:
    def __init__(self, io, frameCallbacks=[], initCallbacks=[],
                 eventCallbacks=[]):
        self.io = io
        self.init = True
        self.busy = True
        self.initCallbacks = initCallbacks
        self.eventCallbacks = eventCallbacks
        self.reader = CorbomiteReadThread(io,
                                          [self.frameReceiver]+frameCallbacks)
        self.writer = CorbomiteWriteThread(io, [])

    def __del__(self):
        print "Del for corbomitedevice called"
        self.reader.stop()
        self.writer.stop()

    def frameReceiver(self, frame):
        print "Unimplemented frame receiver"

    def write(self, data):
        self.writer.write(data)
