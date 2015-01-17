import threading


class SignalSocket():

    def __init__(self):
        self._lock = threading.Lock()
        self.y = []
        self.fwdList = []
        self.logSize = 1024

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()

    def AddSample(self, y):
        """Add a sample to the signal log and make sure the log
        does not exceed the specified size. This function should
        also call ManipulateNewSamples and send the signals to
        registered forward sockets."""
        # TODO investigate the efficiency of this.
        (y) = self.ManipulateNewSample(y)
        self.y.append(y)
        self.y = self.y[-self.logSize:]
        for sock in self.fwdList:
            sock.AddSample(y)

    def ManipulateNewSample(self, y):
        """This allows for derived classes to overload this
        function and new signal values can be manipulated. Can be used
        for data transform operations, ie add signals, triggering etc.
        """
        return (y)

    def SetLogSize(self, n):
        """Set the log size. Could be specified in both time and/or
        samples"""
        self.logSize = n

    def AddForwardSocket(self, fwdSock):
        """Add a signal socket to forward new (manipulated) values to
        """
        self.fwdList.append(fwdSock)

    def GetEndSamplesByNumber(self, n):
        n = min(n, len(self.y))
        return (self.y[-n:])
