import SignalSocket.py
__author__="bjohan"
__date__ ="$Apr 2, 2011 12:29:33 PM$"


class PinModes:
    def __init__(self):
        self.DigitalIn = "Digital input"
        self.DigitalOut = "Digital output"
        self.AnalogIn = "Analog input"
        self.AnalogOut = "Analog output"

class SampleModes:
    def __init__(self):
        self.Polled = "Polled"
        self.Isochronous = "Isochronous"
        self.Triggered = "Triggered"

pinModes = PinModes()
sampleModes = SampleModes()

class Pin:
    def __init__(self, parent, name, pinModes, sampleModes, clockDomains):
        self.name = name
        self.pinModes = pinModes
        self.sampleModes = sampleModes
        self.clockDomains = clockDomains
        self.parent = parent

class IoInterface:
    def getPins(self):
        """this methoud shall return a list of the following structure
        [((Suppoerted pin modes of pin 1),(supported sample modes of pin 1)),
        ((Supported pin modes of pin 2), (supported sample modes of pin 2)),
        ...] The pin and sample modes shall be enumerated by the PinModes and
        SampleModes enumerations above."""
        raise NotImplementedError("IoInterface subclass must inplement this")

    def pollPins(self, pinsToPoll):
        """pinsToPoll should get a list of bools where each bool indicates if a
        pin should be polled or not. This function shall return a list of the
        same length as the pinToPolle where the polled positions containse the
        read value"""
        raise NotImplementedError("IoInterface subclass must inplement this")

    def writePins(self, dataToWrite):
        """writePins should implement a write to io pins. dataToWrite
        shall be a list that contains an element for each pin. If the pin is
        not to be written the element in the list shall contain the value to be
        written, if a pin is not to be written the element shall be None"""
        raise NotImplementedError("IoInterface subclass must inplement this")

    def setPinMode(self, pinNum, mode):
        """Set the mode of a pin"""
        raise NotImplementedError("IoInterface subclass must inplement this")

    def getSampledData(self):
        raise NotImplementedError("IoInterface subclass must inplement this")

    def getClockDomains(self):
        raise NotImplementedError("IoInterface subclass must inplement this")
