#!/usr/bin/env python3
#
#  Copyright (C) 2019-2021 checkra1n team
#  This file is part of pongoOS.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
import sys
import usb.core  # sudo pip install pyusb libusb

#$ lsusb
# ID 05ac:4141 Apple, Inc. pongoOS USB Device
dev = usb.core.find( idVendor=0x05ac, idProduct=0x4141 )
if dev is None:
    raise ValueError('Device not found')

dev.set_configuration()
# if you get 'usb.core.USBError: [Errno 5] Input/Output Error'
# create a file Pongo.rules in /etc/udev/rules.d/ with MODE="0666"

bmRequest_Direction_HostToDevice = 0x00
bmRequest_Direction_DeviceToHost = 0x80

bmRequest_Recipient_Interface = 0x01
bmRequest_Type_Class          = 0x20

#dev.ctrl_transfer( 0x21, 4, 0, 0, 0)
bmRequestType =  \
    bmRequest_Direction_HostToDevice | \
    bmRequest_Type_Class | \
    bmRequest_Recipient_Interface 

dev.ctrl_transfer( 
    bmRequestType   = bmRequestType, 
    bRequest        = 3, 
    wValue          = 0, 
    wIndex          = 0,
    data_or_wLength = sys.argv[1] + "\n",
    timeout         = None
)


#issue fetch stdout
bmRequestType =  \
    bmRequest_Direction_DeviceToHost | \
    bmRequest_Type_Class | \
    bmRequest_Recipient_Interface 

print( "".join( chr (x) for x in dev.ctrl_transfer(
          bmRequestType   = bmRequestType, 
          bRequest        = 1, 
          wValue          = 0, 
          wIndex          = 0,
          data_or_wLength = 0x200
    )
    ))
 
