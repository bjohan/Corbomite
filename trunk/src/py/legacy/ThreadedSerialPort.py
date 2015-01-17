import serial
import os
import time
import thread
import struct
from threading import Thread
import copy


class ThreadedSerialPort(Thread):

    def __init__(self, callback=None):
        Thread.__init__(self,)
        self.lock = thread.allocate_lock()
        self.readBuffer = []
        self.sendBuffer = []
        self.response = []
        self.exit = False
        self.sentChar = ''
        self.nextSendTime = 0.0
        self.lastSendTime = 0.0
        self.port = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0,
            xonxoff=True,
            rtscts=False,
            writeTimeout=10,
            dsrdtr=False,
            interCharTimeout=None)
        self.callback = callback

    def run(self):
        while True:
            self.lock.acquire()
            if self.exit and self.sendBuffer == []:
                return
            try:
                data = self.port.read(10)
            except:
                data = None
            for c in data:
                # print "Got:", ord(c),c
                if self.sentChar == c or self.sentChar == '':
                    if self.sentChar == c and c != '':
                        self.sentChar = ''
                        self.nextSendTime = 0
                # else:
                    # print "Unexpected data", c,ord(c)
                if self.callback is not None:
                    self.callback(c)
                else:
                    self.readBuffer += c

            if (self.sendBuffer != [] and
                    self.nextSendTime < time.time()):
                n = self.port.write(self.sendBuffer[0])
                self.sentChar = self.sendBuffer[0]
                self.sendBuffer = self.sendBuffer[1:]
                self.nextSendTime = time.time() + 0.1
                if self.sentChar == '\n':
                    self.sentChar = None
                self.lastSendTime = time.time()
            self.lock.release()

    def sendData(self, data):
        self.lock.acquire()
        ints = []
        for ch in data:
            ints.append(ord(ch))
        self.sendBuffer += struct.pack('B' * len(ints), *ints)
        self.lock.release()

    def readData(self):
        self.lock.acquire()
        r = self.readBuffer
        self.readBuffer = []
        self.lock.release()
        return r

    def stop(self):
        self.lock.acquire()
        self.exit = True
        self.lock.release()
