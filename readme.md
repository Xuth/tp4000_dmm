Takes readings off the serial port from a class of multimeters that includes
the TekPower TP4000ZC (the meter I own) and supposedly is the same as the the
'VC820' mode in QtDMM.

It looks like the DMM chipset that implements this protocol is the Fortune Semiconductor FS9721_LP3.

Based on other sources, it looks like the following meters use this protocol (I've tested none of them):

    * HoldPeak DMM HP-90EPC
    * Digitek DT4000ZC
    * PCE PCE-DM32
    * Tecpel DMM-8061
    * UNI-T UT60E
    * Voltcraft VC-820
    * Voltcraft VC-840


class Dmm:
    """
    Takes readings off the serial port from a class of multimeters that includes
    the TekPower TP4000ZC (the meter I own) and supposedly is the same as the the
    'VC820' mode in QtDMM.

    example code:

    # load the module
    import tp4000zc
    
    # the port that we're going to use.  This can be a number or device name.
    # on linux or posix systems this will look like /dev/tty2 or /dev/ttyUSB0
    # on windows this will look something like COM3
    port = '/dev/ttyUSB0'

    # get an instance of the class
    dmm = tp4000zc.Dmm(port)

    # read a value
    val = dmm.read()
    
    print (val.text)       # print the text representation of the value
                           # something like: -4.9 millivolts DC
    print (val.numericVal) # and the numeric value
                           # ie: -0.0048
    # recycle the serial port
    dmm.close()


    Public Interface:
    __init__(port, retries=3, timeout=3.0):
        Instantiating the class attempts to open the serial port specified, 
        initialize it and read enough from the serial port to synchronize 
        the module with the start/end of a full reading.

    read():
        Attempt to get a complete reading off of the serial port, parse it and
        return an instance of DmmValue holding the interpretted reading.

    close():
        Finally you can close the serial port connection with close()

    Exceptions will be raised if 
       * PySerial raises an exception (SerialException or ValueError)
       * this module can't get a full reading that passes initial data integrity
         checks (subclasses of DmmException)
       * I made a coding error (whatever python might throw)

    If no exceptions are raised the DmmValue might still fail various sanity
    checks or not have a numeric value.  Ie I believe that showing 
    multiple decimal points makes no sense but is valid per the protocol so
    no exception is raised but the saneValue flag will be set to False in the
    DmmValue.

    Meter Documentation:

    Per the documentation page, the meter spits out readings which are bursts of 
    14 bytes every .25 seconds.  The high nibble of each byte is the byte number 
    (1-14) for synchronization and sanity checks, the low nibble holds the data.

    Each data bit represents an individual field on the LCD display of the meter, 
    from segments of the 7 segment digits to individual flags.  Bytes 1 and 10-14
    are flags (with four bits reserved/unmapped on this meter) and bytes (2,3), 
    (4,5), (6,7) and (8,9) representing the individual digits on the display.

    For the digits, if the high bit of the first nibble of a digit is set then the
    negative sign (for the first digit) or the leading decimal point is turned on.
    the remaining bits of the two nibbles represent the elements of the 7 segment
    digit display as follows:

      pos 3       nibble 1:   S123
     p     p      nibble 2:   4567
     o     o      where S is either the sign or decimal bit.
     s     s
     2     7      The legal values of the segment bits are represented in
      pos 6       digitTable and include the digits 0-9 along with blank and
     p     p      'L'.
     o     o
     s     s
     1     5
      pos 4

    Serial settings for this meter are:
    2400 baud 8N1
    """


class DmmValue:
    """
    This is a representation of a single read from the multimeter.

    Attributes in rough order of usefulness:
    
    Sanity checks:
       saneValue: True if no sanity checks failed.
    
    High level computed fields:
       text: Nicely formatted text representation of the value.
       numericVal: numeric value after SI prefixes applied or None if value is non-numeric.
       measurement: what is being measured.
       delta: True if the meter is in delta mode.
       ACDC: 'AC', 'DC' or None.
       readErrors:  Number of failed reads attempts before successfully getting a reading 
           from the meter.

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
