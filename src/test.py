#!/usr/bin/env python

#  CAN-FIX Protocol Module - An Open Source Module that abstracts communication
#  with the CAN-FIX Aviation Protocol
#  Copyright (c) 2014 Phil Birkelbach
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

import canbus
import canfix
import tests

def run_tests():
    tests.run_tests()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='CAN-FIX Configuration Utility Protocol Module')
    parser.add_argument('--print-canfix', '-p', action='store_true', help='Print CAN-FIX Protocol Information')
    args = parser.parse_args()
    
    if args.print_canfix == True:
        print "CANFIX Protocol Version " + canfix.version
        print "Groups:"
        for each in canfix.groups:
            print "  %s %d-%d" % (each["name"], each["startid"], each["endid"])
        
        print "Parameters:"
        for each in canfix.parameters:
            print canfix.parameters[each]
    else:
        run_tests()


        
        