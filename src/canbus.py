#!/usr/bin/python

#  CAN-FIX Utilities - An Open Source CAN FIX Utility Package 
#  Copyright (c) 2012 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import adapters.easy
import adapters.simulate
import serial
from serial.tools.list_ports import comports

class Connection():
    """Class that represents a connection to a CAN device"""
    def __init__(self, portname = "", bitrate = 125, timeout = 0.25):
        self.portname = portname
        self.timeout = timeout
        #Here we append all the different Adapter classes to our list
        self.devices = []
        self.devices.append(adapters.easy.EasyAdapter(bitrate))
        self.devices.append(adapters.simulate.SimulateAdapter(bitrate))

    def connect(self, index):
        #This code tries to find a USB/CAN device on one of the comm ports.
        #TODO: This should call some function from each devcie on each portname
        #      to try and find the a device on the port.
        if self.portname == "":
            for each in comports():
                if string.find(each[1], "USB2-F-7x01") >= 0:
                    self.portname = each[0]
                    print "Found CAN device on Port", self.portname

        if self.portname == "":
            raise BusInitError("No CAN device found")

        self.ser = serial.Serial(self.portname, 115200, timeout=self.timeout)
        self.devices[1].setport(self. ser)
        self.initialize = self.devices[1].initialize
        self.open = self.devices[1].open
        self.close = self.devices[1].close
        self.error = self.devices[1].error
        self.sendFrame = self.devices[1].sendFrame
        self.recvFrame = self.devices[1].recvFrame


if __name__ == '__main__':
    can = Connection("/dev/ttyUSB0")
    for each in can.devices:
        print each.name
    can.connect()
    can.initialize()
    can.open()

    frames=[{'id':0x701, 'data':[0, 1, 3, 0x0F, 0x00]},
            {'id':0x701, 'data':[0, 1, 3, 0x0F, 0x01]},
            {'id':0x701, 'data':[0, 1, 3, 0x0F, 0x02]},
            {'id':0x701, 'data':[0, 1, 3, 0x0F, 0x03]},
            {'id':0x701, 'data':[0, 1, 3, 0x0F, 0x04]},
            {'id':0x701, 'data':[0, 1, 3, 0x0F, 0x05]},
            {'id':0x701, 'data':[0xFF, 7, 1, 0xF7, 0x00]},
            {'id':0x6E0, 'data':[1, 0xf, 0, 64]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[0, 0, 0, 0, 0, 0, 0, 0]},
            {'id':0x6E0, 'data':[2, 0, 0, 0]},
            {'id':0x6E0, 'data':[3, 0, 0, 0]},
            {'id':0x6E0, 'data':[4]},
            {'id':0x6E0, 'data':[5, 0, 0, 0, 0]}]

    for each in frames:
        can.sendFrame(each)
        try:
            result = can.recvFrame()
        except DeviceTimeout:
            result = "Timeout"
        print result
