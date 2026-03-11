#!/bin/bash

# parsed onto ydotool commands by flipper0badusb_test with <3 by (#4|2
# https://github.com/carvilsi/flipper0-badUSB-linux-tester
# run command simple 
# esc just in case
ydotool key 1:1 1:0
# Open run-command
ydotool key 56:1 60:1 60:0 56:0
sleep 0.5
ydotool type 'echo "foobar"'
ydotool key 28:1 28:0
