# flipper0-badUSB-linux-tester
Test on Linux your Flipper Zero BadUSB Scripts without loading the payload onto the Flipper device.

After experimenting for a while and writing some BadUSB Ducky scripts on Flipper Zero, I felt a bit overwhelmed by the [workflow](https://docs.flipper.net/zero/bad-usb) every time I wanted to test a change in the script.
I've been searching and testing some other solutions but I found lot of issues related with Linux graphical environment permissions and I decided to write something simple to test and write my FlipperZero's DuckyScripts.

Right now only tested on **ArchLinux**.

## Usage

`$ git clone https://github.com/carvilsi/flipper0-badUSB-linux-tester`
`$ cd flipper0-badUSB-linux-tester`

`$ chmod a+x flipper0badusb_test`

```
Wrong arguments.

Usage:

    $ ./flipper0badusb_test <flipper_ducky_script_file.txt> <out_file.sh> [test]


If "test" is provided will run the DuckyScript after parsing it
```

The you can test your FlipperZero's DuckyScript with:

`$ sh out_file.sh`

Or pass "test" after the command line and it will be executed after creating the sh file.

`$ ./flipper0badusb_test.py examples/hello-world.txt out.sh ex`

### Dependencies
Depends on [ydotool](https://github.com/ReimuNotMoe/ydotool) for command-line automation tool on Linux. 

#### ArchLinux
- Install it: `$ sudo pacman -S ydotool`

- Run the service: `$ systemctl --user start ydotool`

## Current Flipper's DuckyScript implemented commands
- DEFAULT_DELAY
- DEFAULTDELAY
- STRINGLN
- STRING
- DELAY
- ENTER
- GUI
- REM

More info about Flipper's [BadUSB File Format](https://developer.flipper.net/flipperzero/doxygen/badusb_file_format.html)

---

⚠️ ADVISORY: This script should be used for authorized penetration testing and/or educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own computers and/or with the computer owner's permission.

---

Feedback from usage and contributions are very welcome.
Also if you like it, please leave a :star: I would appreciate it ;)


