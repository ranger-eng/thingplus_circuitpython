#!/bin/bash

mpremote fs cp -r ./rootdir/* :
mpremote exec --no-follow "import microcontroller; microcontroller.reset()"
