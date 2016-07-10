# power-trinket

Little project that uses the [Trinket][] and [INA219 current
sensor breakout][] from Adafruit to monitor the power consumption
of a DC device, using up to 26V and 3.2A, and shows realtime
lectures of voltage, current and power.

![Software screenshot](http://i.imgur.com/8pK1TU9.png)

Communication is done via [TrinketFakeUsbSerial][] which is
[explained][fake-usb] in Adafruit Learning System.


## Install

You should have Python, PIP and libusb installed.  
On Debian-based OSes, you can do:

    sudo apt-get install python-dev python-pip libusb-1.0-0

Then install the [PyUSB][] and [docopt][] Python modules:

    sudo pip install pyusb docopt

You will also need the Arduino IDE, correctly configured to use
the Trinket, and the [TrinketFakeUsbSerial][] and [TinyWireM][]
libraries installed.

Now go on and [use it](#use)!


## Use

You need a 5V Trinket working at 16MHz to use this. Upload the
`power-trinket.ino` sketch and build the following circuit:

![Sketch breadboard view](http://i.imgur.com/D6hVDWz.png)

Connect the load and power supply, plug the Trinket via USB, and run the Python script:

    python power-trinket.py

If everything goes well, the Trinket will be detected as soon as it
boots the sketch and the script will start displaying realtime
lectures at the console.

You can see which options it accepts with:

    python power-trinket.py --help



[Trinket]: http://learn.adafruit.com/introducing-trinket "The Adafruit Trinket"
[INA219 current sensor breakout]: https://www.adafruit.com/product/904 "INA219 High Side DC Current Sensor Breakout"
[TrinketFakeUsbSerial]: https://github.com/adafruit/Adafruit-Trinket-USB
[TinyWireM]: https://github.com/adafruit/TinyWireM
[fake-usb]: http://learn.adafruit.com/trinket-fake-usb-serial "Trinket Fake USB serial"

[PyUSB]: http://sourceforge.net/apps/trac/pyusb
[docopt]: http://docopt.org
