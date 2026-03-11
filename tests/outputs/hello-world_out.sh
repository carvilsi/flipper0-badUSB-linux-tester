#!/bin/bash

# parsed onto ydotool commands by flipper0badusb_test with <3 by (#4|2
# https://github.com/carvilsi/flipper0-badUSB-linux-tester
# trying stuff
# Open Terminal app
ydotool key 125:1 30:1 30:0 125:0
ydotool type 'Terminal'
sleep 5
ydotool key 28:1 28:0
# Wait 10 seconds after all commands
sleep 10
# echo something 
ydotool type 'echo "The world is all that is the case"'
ydotool key 28:1 28:0
ydotool type 'echo "The world is the totality of facts, not of things"'
ydotool key 28:1 28:0
# hide the Terminal app
ydotool key 125:1 35:1 35:0 125:0
