import Oscilloscope
import time
class Hp8922mScope(Oscilloscope.Oscilloscope):
	def __init__(self, ms):
		self.ms =  ms
		Oscilloscope.Oscilloscope.__init__(self,
				channels = ['INPUT'],
				verticalScales = {'INPUT':[
						'20 V',
						'10 V',
						'5 V',
						'2 V',
						'1 V',
						'500 mV',
						'200 mV',
						'100 mV',
						'50 mV',
						'20 mV',
						'10 mV',
						'5 mV',
						'2 mV',
						'1 mV',
						'500 uV',
						'200 uV',
						'100 uV',
						'50 uV',
						'20 uV']},
				coupling = ['DC'],
				triggerChannels = ['1', 'EXT'],
				triggerModes = ['CONT', 'SINGLE'],
				triggerSlopes = ['POS', 'SENS'],
				signalSources = ['Scope'],
				model = 'HP8922M Built in oscilloscope')
		time.sleep(1)
		self.ms.ExecuteCommand("DISP:SCR OSC",3)
		time.sleep(1)
		self.ms.ExecuteCommand("OSC:CONT MAIN", 3)
		time.sleep(1)

	def enableChannel(self, chNum):
		if chNum in self.channels:
			return True
		else:	
			return False

	def setCoupling(self, coupling):
		if coupling in self.coupling:
			return True
		else:
			return False

	def setVerticalScale(self, scale, ch):
		if scale in self.verticalScales[ch]:
			
			print self.ms.ExecuteCommand('"OSC:SCAL:VERT:VOLT '+'""'+scale+'"""',3)
			time.sleep(1)
			return True
		else:
			print "Scale does not exist", scale
			return False

	def setTriggerChannel(self, trig):
		print "Set trigger channel not implemented for", self.model
	
	def setTriggerLevel(self, trigLev):
		print "Set trigger level implemented for", self.model

	def setInput(self, chNum, source):
		print "Set input sourcec not implemented for", self.model
	
	def readTrace(self):
		return  self.ms.ExecuteCommand("MEAS:OSC:TRACE?",1)
		time.sleep(1)
					
