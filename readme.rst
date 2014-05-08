Easily gather measurements from your multimeter using the
Fortune Semiconductors FS9721_LP3 protocol.

Installation
------------

Install from Github directly::
    
    git clone https://github.com/coddingtonbear/python-fs9721.git
    cd python-fs9721
    python setup.py install

or, install from PyPI using ``pip``::

    pip install fs9721

Use as a Library
----------------

Create the client you'll use for gathering measurements first.  Using
the path to the serial device, create an instance of ``fs9721.Client``::

    from fs9721 import Client

    my_multimeter = Client('/dev/tty.usbserial')

Then, you can gather measurements from your multimeter using::

    print(my_multimeter.getMeasurement())

Command-Line Use
----------------

Just run::

    fs9721 /path/to/serial/port

For example, on my computer the device is connected via the serial port
at ``/dev/tty.usbserial``, for me to gather measurements directly from
the multimeter, I would run::

    fs9721 /dev/tty.usbserial

Does this support my multimeter?
--------------------------------

This library should support any multimeter using the
Fortune Semiconductors FS9721_LP3 chip.
Common multimeters using this chip are often low-end and include the following:

* TekPower TP4000ZC
* UNI-T_UT60E
* V&A V18b
* Voltcraft VC-820 and VC-840

If your multimeter is not on the above list, do not despair!
This specific IC is very common, and it may very use this chip.
Sigrok has a nice reference of which chips various multimeters use;
`search for your multimeter on their wiki <http://sigrok.org/wiki/Main_Page>`_
to see if yours also uses this DMM IC.
