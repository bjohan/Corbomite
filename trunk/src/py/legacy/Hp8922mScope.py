import Oscilloscope


class Hp8922mScope(Oscilloscope.Oscilloscope):

    def __init__(self, ibasic):
        self.ibasic = ibasic
        Oscilloscope.Oscilloscope.__init__(self,
                                           channels=[1],
                                           verticalScales=[[
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
                                               '20 uV']],
                                           coupling=['DC'],
                                           triggerChannels=['1', 'EXT'],
                                           triggerModes=['CONT', 'SINGLE'],
                                           triggerSlopes=['POS', 'SENS'],
                                           signalSources=['Scope'],
                                           model='HP8922M Built in oscilloscope')
        print "Uploading and executing server software"
        self.ibasic.SendProgramGetOutput(
            'OUTPUT 814;"DISP:SCR OSC"\n' +
            'OUTPUT 814;"OSC:CONT MAIN"\n')

    def readTrace(self):
        data = self.ibasic.SendProgramGetOutput(
            'dim dat(1:417)\n' +
            'print "Requesting trace"\n' +
            'output 814; "MEAS:OSC:TRACE?"\n' +
            'print "Reading data"\n' +
            'enter 814 USING "%,K";dat(*)\n' +
            'x = 1\n' +
            '	while x < 418\n' +
            '	print dat(x),\n' +
            '	x=x+1\n' +
            'end while\n')
        marker = "Reading data"
        pos = data.find(marker) + len(marker)
        # print "pos", pos, "substrpos:", data.find(marker)
        # print "##############################"
        # print data[pos:]
        data = data[pos:]
        output = []
        for ent in data.split():
            output += [float(ent)]
        return output
