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

# This function is a placeholder for callbacks that have not been set

import canbus

def DoNothing():
    pass

class FirmwareBase:
    def __init__(self):
        # .kill when set to True should stop downloads
        self.kill = False
        # Set the callback functions to DoNothing to avoid times when they
        # are not used by the caller.
        self.progressCallback = DoNothing
        self.statusCallback = DoNothing
        self.completeCallback = DoNothing
        
    
    def setProgressCallback(self, progress):
        if callable(progress):
            self.progressCallback = progress
        else:
            raise TypeError("Argument passed is not a function")
        
    def setStatusCallback(self, status):
        if callable(status):
            self.statusCallback = status
        else:
            raise TypeError("Argument passed is not a function")
        
    def setCompleteCallback(self, complete):
        if callable(complete):
            self.completeCallback = complete
        else:
            raise TypeError("Argument passed is not a function")
        
    def stop(self):
        self.__kill = True
        canbus.disableRecvQueue(2)
        
    # Download support functions
    def __tryChannel(self, ch):
        """Waits for a half a second to see if there is any traffic on any
           of the channels"""
        endtime = time.time() + 0.5
        ch.ClearAll()
        while True: # Channel wait loop
            try:
                rframe = canbus.recvFrame(2)
            except canbus.DeviceTimeout:
                pass
            else:
                ch.TestFrame(rframe)
                now = time.time()
                if now > endtime: break

    def __tryFirmwareReq(self, ch, node):
        """Requests a firmware load, waits for 1/2 a second and determines
           if the response is correct and if so returns True returns
           False on timeout"""
        channel = ch.GetFreeChannel()
        sframe = canbus.Frame(1792 + canbus.srcNode, [node, 7, 1, 0xF7, channel])
        canbus.sendFrame(sframe)
        endtime = time.time() + 0.5
        ch.ClearAll()
        while True: # Channel wait loop
            try:
                rframe = canbus.recvFrame(2)
            except canbus.DeviceTimeout:
                pass
            else:
                if rframe.id == (1792 + node) and \
                   rframe.data[0] == self.__srcnode: break
                now = time.time()
                if now > endtime: return False
        return True

    def start_download(self, node):
        ch = Channels()
        data = []
        attempt = 0
        while True: # Firmware load request loop
            if self.__kill: 
                print "Gotta be killed"
                exit(-1)
            print "Trying Channel"
            self.__driver.statusCallback("Trying Channel " + str(attempt))
            attempt += 1
            self.__tryChannel(ch)
            # send firmware request
            if self.__tryFirmwareReq(ch, node): break
            
        # Here we are in the Firmware load mode of the node    
        # Get our firmware bytes into a normal list
        channel = ch.GetFreeChannel()
  
