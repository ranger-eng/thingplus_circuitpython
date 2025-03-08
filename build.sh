#!/bin/bash

mpremote fs cp --force ./rootdir/* :
mpremote fs cp --force ./rootdir/lib/* :lib
mpremote exec --no-follow "import microcontroller; microcontroller.reset()"
