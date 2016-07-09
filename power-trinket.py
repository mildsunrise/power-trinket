#!/usr/bin/env python
# Copyright (c) 2016 Alba Mendez
# All rights reserved.
# This file is part of power-trinket.
#
# power-trinket is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# power-trinket is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with power-trinket.  If not, see <http://gnu.org/licenses/>.

"""power-trinket host reader.

Usage:
  power-trinket.py [options]

Options:
  -o --once     Exit at disconnect, instead of reconnecting forever.
  -r --raw      Print the raw values (shunt voltage, bus voltage and
                current) without rounding or formatting.
  -s --sense    Include sense resistor voltage load in voltage and
                calculated power shown.
  -A --no-ansi  Don't use ANSI escape sequences for color and scrollback.
  -v --verbose  Show additional info.
  -q --quiet    Don't show any status messages.

  -h --help     Show this help text.
  -V --version  Show the program's version.

"""

from docopt import docopt
from sys import stdout, stderr
import time, select, struct, sys
import usb.core, usb.util

SYNC_STRING = "S" + " "*14 + "E"
DATA_LENGTH = 4 * 3
TOTAL_LENGTH = len(SYNC_STRING) + DATA_LENGTH

def loop():

    # 1. Try to find and connect to a Trinket

    if args["--verbose"]:
        stderr.write("Waiting for a Trinket...")
        stderr.flush()

    while True:
        trinket = usb.core.find(idVendor = 0x1781, idProduct = 0x1111)
        if trinket: break
        time.sleep(0.1) # don't hog all CPU

    trinket.set_configuration()
    endpoint = trinket[0][(0,0)][0] # the first endpoint should be the only endpoint, it should be an interrupt-in endpoint

    if not args["--quiet"]:
        stderr.write("Connected to a Trinket.\n")
        stderr.flush()

    if not args["--raw"]:
        if args["--no-ansi"]:
            format = "Shunt: %7.2fmV    %6.2fV / %6.3fA / %6.2fW\n"
        else:
            format = "\r\x1b[2KShunt: %7.2fmV    \x1b[1m%6.2f\x1b[mV / \x1b[1m%6.3f\x1b[mA / \x1b[1m%6.2f\x1b[mW "
            stdout.write("Shunt:  ---.--mV     --.--V /  -.---A /  --.--W ")
            stdout.flush()

    # 2. Start reading lectures

    while True:
        try:
            chunk = bytearray()
            while True:
                # read next byte, rotate the chunk
                chunk.append(endpoint.read(1)[0])
                if len(chunk) > TOTAL_LENGTH: chunk = chunk[len(chunk) - TOTAL_LENGTH:]
                # break if we have a complete, correct chunk
                if len(chunk) == TOTAL_LENGTH and chunk.startswith(SYNC_STRING): break

            # parse the chunk, output result
            lecture = struct.unpack("fff", chunk[len(SYNC_STRING):])

            if args["--raw"]:
                stdout.write("\t".join(str(f) for f in lecture) + "\n")
            else:
                voltage = lecture[1]; current = lecture[2] / 1000
                if args["--sense"]: voltage += lecture[0] / 1000
                stdout.write(format % (lecture[0], voltage, current, voltage * current))

            stdout.flush()

        except usb.core.USBError as ex:
            if args["--verbose"]:
                print('USB read error:', ex)
            break

    stdout.write("\n")


    if not args["--quiet"]:
        stderr.write("Disconnecting from the Trinket.\n\n")
        stderr.flush()


if __name__ == '__main__':
    args = docopt(__doc__, version="power-trinket 0.0.1")
    try:
        if args["--once"]:
            loop()
        else:
            while True:
                loop()
                time.sleep(0.5)
    except KeyboardInterrupt:
        stderr.write("\n")
