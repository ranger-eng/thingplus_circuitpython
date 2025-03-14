#!/bin/bash

ttydevice=$(ls /dev/tty.usbmodem*)

mpremote fs cp --force ./rootdir/* :
mpremote fs cp --force ./rootdir/lib/* :lib
mpremote fs cp --force ./adafruit_seesaw/* :lib/adafruit_seesaw
mpremote exec --no-follow "import microcontroller; microcontroller.reset()"
