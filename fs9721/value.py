# -*- coding: utf-8 -*-
from measurement.base import MeasureBase
from measurement.measures import (
    Capacitance,
    Current,
    Frequency,
    Resistance,
    Temperature,
    Voltage,
)


class DmmValue(object):
    """
    This is a representation of a single read from the multimeter.

    Attributes in rough order of usefulness:

    Sanity checks:
       saneValue: True if no sanity checks failed.

    High level computed fields:
       text: Nicely formatted text representation of the value.
       numericVal: numeric value after SI prefixes applied or None if
            value is non-numeric.
       measurement: what is being measured.
       delta: True if the meter is in delta mode.
       ACDC: 'AC', 'DC' or None.
       readErrors:  Number of failed reads attempts before successfully
            getting a reading  from the meter.

    Other, possibly useful, computed fields:
       val: cleaned up display value
       scale: SI prefix for val

    Unprocessed values:
       rawVal: Numeric display
       flags: Various flags modifying the measurement
       scaleFlags: SI scaling factor flags
       measurementFlags: Flags to specify what the meter is measuring
       reservedFlags: Flags that are undefined
       rawBytes:  the raw, 14 byte bitstream that produced this value.

    """
    MEASURE_CLASSES = {
        # Duty Cycle?
        # Diode?
        'F': Capacitance,
        'Ω': Resistance,
        'A': Current,
        'V': Voltage,
        'Hz': Frequency,
        'C': Temperature,
    }

    def __init__(self, val, attribs, readErrors, rawBytes):
        self.saneValue = True
        self.rawVal = self.val = val
        self.flags = attribs['flags']
        self.scaleFlags = attribs['scale']
        self.measurementFlags = attribs['measure']
        self.reservedFlags = attribs['other']
        self.readErrors = readErrors
        self.rawBytes = rawBytes
        self.text = 'Invalid Value'

        self.processFlags()
        self.processScale()
        self.processMeasurement()
        self.processVal()

        self.measurementObject = self.createMeasurementObject()

        if self.saneValue:
            self.createTextExpression()

    def getMeasurement(self):
        return self.measurementObject

    def createMeasurementObject(self):
        try:
            return (
                self.MEASURE_CLASSES[self.measurement](
                    **{self.measurement: self.numericVal}
                )
            )
        except KeyError:
            return self.numericVal
        except (ValueError, TypeError):
            return None

    def createTextExpression(self):
        text = self.deltaText
        text += self.val
        text += ' '
        text += self.scale
        text += self.measurement
        text += self.ACDCText
        self.text = text

    def processFlags(self):
        flags = self.flags
        self.ACDC = None
        self.ACDCText = ''
        self.delta = False
        self.deltaText = ''

        if 'AC' in flags and 'DC' in flags:
            self.saneValue = False
        if 'AC' in flags:
            self.ACDC = 'AC'
        if 'DC' in flags:
            self.ACDC = 'DC'
        if self.ACDC is not None:
            self.ACDCText = ' ' + self.ACDC
        if 'REL delta' in flags:
            self.delta = True
            self.deltaText = 'delta '

    def processScale(self):
        s = self.scaleFlags
        self.scale = ''
        self.multiplier = 1

        if len(s) == 0:
            return
        if len(s) > 1:
            self.saneValue = False
            return
        self.scale = s[0]
        self.multiplier = MeasureBase.SI_MAGNITUDES[self.scale]

    def processMeasurement(self):
        m = self.measurementFlags
        self.measurement = None
        if len(m) != 1:
            self.saneValue = False
            return
        self.measurement = m[0]

    def processVal(self):
        v = self.rawVal
        self.numericVal = None
        if 'X' in v:
            self.saneValue = False
            return
        if v.count('.') > 1:
            self.saneValue = False
            return

        n = None
        try:
            n = float(v)
        except:
            pass

        if n is not None:
            # this should remove leading zeros, spaces etc.
            self.val = '%s' % (n, )
            self.numericVal = n * self.multiplier

    def __repr__(self):
        return "<DmmValue instance: %s>" % self.text
