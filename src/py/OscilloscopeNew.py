class Oscilloscope:
	def __init__(self, channels = [], verticalScales = [], coupling = '',
			triggerChannels = [], triggerModes = [],
			triggerSlopes = [], signalSources = [], 
			model = 'none'):
		self.channels = channels
		self.verticalScales = verticalScales
		self.coupling = coupling
		self.triggerChannels = triggerChannels
		self.triggerModes = triggerModes
		self.triggerSlopes = triggerSlopes
		self.triggerLevel = 0.0
		self.signalSources = signalSources
		self.model = model

	def enableChannel():
		print "Enable channel not implemented for", self.model

	def readTrace(self, chNum):
		print "Read trace for channel not implemented for",self.model

	def setCoupling(self, cuopling):
		print "Set coupling not implemented for", self.model

	def setVerticalScale(self, scale, chNum):
		print "Set vertical scale not implemented for", self.model

	def setTriggerChannel(self, chNum):
		print "Set trigger channel not implemented for", self.model
	
	def setTriggerLevel(self, trigLev):
		print "Set trigger level implemented for", self.model

	def setInput(self, chNum, source):
		print "Set input sourcec not implemented for", self.model
		
