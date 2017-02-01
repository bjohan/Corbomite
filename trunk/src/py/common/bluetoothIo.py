import subprocess
import sys
from bluetooth import *

class BluetoothIo():
	def __init__(self, addr):
		self.sock = BluetoothSocket(RFCOMM)
		self.sock.connect((addr, 1))
		self.port = addr

	def write(self, data):
		self.sock.send(data);	

	def read(self):
		return self.sock.recv(1);

	def __del__(self):
		self.sock.close();
