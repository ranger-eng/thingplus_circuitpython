#!/bin/bash

ttydevice=$(ls /dev/tty.usbmodem*)

mpremote fs cp --force ./rootdir/* :
(ampy -p $ttydevice ls /lib | sed 's|^/|:|' | xargs -I {} mpremote fs rm {})
mpremote fs cp --force ./rootdir/lib/* :lib
mpremote exec --no-follow "import microcontroller; microcontroller.reset()"
