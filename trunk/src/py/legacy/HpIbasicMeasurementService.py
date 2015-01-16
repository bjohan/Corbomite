import IbasicInterface
class HpIbasicMeasurementService:
	def __init__(self):
		self.ibas = IbasicInterface.IbasicInterface()
		print "Uploading measurement server"
		self.ibas.SendProgram(	
			'dim trace(1:418)\n'+
			'x = 1\n'+
			'print "Program started"\n'+
			'while x = 1\n'+
			'input "command:",cmd$\n'+
			'if cmd$ = "quit" then\n'+
			'goto exit_loop\n'+
			'end if\n'+
			'input "data type:",t\n'+
			'print "command:",cmd$\n'+
			'print "type:",t\n'+
			'input "correct", c\n'+
			'if c = 1 then\n'+
			'output 814;cmd$\n'+
			'if t = 1 then\n'+
			'print "measuring"\n'+
			'enter 814 using "%,K";trace(*)\n'+
			'print "done"\n'+
			'i = 1\n'+
			'while i < 418\n'+
			'print trace(i),\n'+
			'i = i + 1\n'+
			'end while\n'+
			'print\n'+
			'print "measurement finished"\n'+
			'end if\n'+
			'if t = 2 then\n'+
			'print "measuring"\n'+
			'enter 814;n\n'+
			'print n\n'+
			'print "measurement finished"\n'+
			'end if \n'+
			'end if\n'+
			'end while\n'+
			'exit_loop: print "done"\n')
		print "Done"
		print "Starting server"
		self.ibas.RunProgram()
		print "Done"

	def ParseTraceData(self, data):
		traceData = []
		for word in data.split():
			try:
				traceData.append(float(word))
			except ValueError:
				pass
				
		return traceData

	def ExecuteCommand(self, cmd, fmt):
		print "Executing command", cmd, "with type", str(fmt)
		tries = 1;
		rd = None
		while tries > 0:
			#print "Buffer lost:",''.join(self.ibas.GetOutput())
			#print "Sending command"
			self.ibas.SendInput(cmd+'\r')
			#print "Waiting for data"
			self.ibas.FindOutputSequence([cmd, 'type:'])
			#print "sending format:", str(fmt)
			self.ibas.SendInput(str(fmt)+'\r')
			fragments =  self.ibas.FindOutputSequence(
					[str(fmt), 'command:', 
					cmd,'type:', str(fmt),  
					'correct'])
			print "fragments:", fragments
			if not str(fmt) in fragments[4]:
				self.ibas.SendInput('0\r')
				self.ibas.FindOutputSequence(['command:'])
			else:
				self.ibas.SendInput('1\r')
				if fmt in [1, 2]:
					d=self.ibas.FindOutputSequence(
					['measuring', 'measurement finished',
					'command:'], maxTime = 90)
					if fmt == 1:
						rd=self.ParseTraceData(d[-2])
				else:				
					self.ibas.FindOutputSequence(
					['command:'])
				break
			tries -= 1
		return rd
			

				
	def Quit(self):
		self.ibas.SendInput('quit\n')
		del self.ibas	
		
	def ExecuteTraceCommand(self, cmd):
		pass
