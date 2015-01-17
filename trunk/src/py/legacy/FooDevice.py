# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "bjohan"
__date__ = "$Apr 2, 2011 1:28:33 PM$"
# from IoInterface import *
import IoInterface


class FooDevice(IoInterface.IoInterface):

    def __init__(self):
        self.clockDomains = ["Timer0", "Timer1"]
        self.pins = [IoInterface.Pin(self,
                                     'A0',
                                     (IoInterface.pinModes.DigitalIn,
                                      IoInterface.pinModes.AnalogIn,
                                      IoInterface.pinModes.AnalogOut),
                                     (IoInterface.sampleModes.Isochronous,
                                         IoInterface.sampleModes.Polled,
                                         IoInterface.sampleModes.Triggered),
                                     self.clockDomains[0:2]),
                     IoInterface.Pin(self,
                                     'A1',
                                     (IoInterface.pinModes.DigitalIn,
                                      IoInterface.pinModes.AnalogIn,
                                      IoInterface.pinModes.DigitalOut),
                                     (IoInterface.sampleModes.Isochronous,
                                         IoInterface.sampleModes.Polled,
                                         IoInterface.sampleModes.Triggered),
                                     [self.clockDomains[1]]),
                     IoInterface.Pin(self,
                                     'B0',
                                     (IoInterface.pinModes.DigitalIn,
                                      IoInterface.pinModes.AnalogOut),
                                     (IoInterface.sampleModes.Isochronous,
                                         IoInterface.sampleModes.Polled,
                                         IoInterface.sampleModes.Triggered),
                                     [self.clockDomains[0]])]

    def getPins(self):
        return self.pins

    def pollPins(self, pinsToPoll):
        """pinsToPoll should get a list of bools where each bool indicates if a
        pin should be polled or not. This function shall return a list of the
        same length as the pinToPolle where the polled positions containse the
        read value"""
        pass

    def writePins(self, dataToWrite):
        """writePins should implement a write to io pins. dataToWrite
        shall be a list that contains an element for each pin. If the pin is
        not to be written the element in the list shall contain the value to be
        written, if a pin is not to be written the element shall be None"""
        pass

    def setPinMode(self, pin):
        print "Pin:", pin.name, "is set to:", pin.pinMode, pin.sampleMode,\
            pin.clockDomain
        for p in self.pins:
            if p.name == pin.name:
                print "Oin:", p.name, "is set to:", p.pinMode, p.sampleMode,\
                    p.clockDomain

        """Set the mode of a pin"""
        pass

    def getSampledData(self):
        pass

    def getClockDomains(self):
        pass
