Easily gather measurements from your multimeter using the Fortune Semiconductors FS9721_LP3 protocol.

This is all based upon `@xuth <https://github.com/Xuth/>`_'s work in
his `TP4000ZC library <https://github.com/Xuth/tp4000_dmm>`_).
(Don't worry, @xuth, a PR will be incoming once I've finished).

Installation
------------

Install from Github directly::
    
    git clone https://github.com/coddingtonbear/python-fs9721.git
    cd python-fs9721
    python setup.py install

Does this support my multimeter?
--------------------------------

This library should support any multimeter using the Fortune Semiconductors FS9721_LP3 chip.  Common multimeters using this chip are often low-end and include the following:

* TekPower TP4000ZC
* UNI-T_UT60E
* V&A V18b
* Voltcraft VC-820 and VC-840

If your multimeter is not on the above list, do not despair!  This specific IC is very common, and it may very use this chip.  Sigrok has a nice reference of which chips various multimeters use; `search for your multimeter on thier wiki <http://sigrok.org/wiki/Main_Page>`_ to see if yours also uses this DMM IC.
