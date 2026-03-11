# flipper0-badUSB-linux-tester
Test on Linux your Flipper Zero BadUSB Scripts without loading the payload onto the Flipper device.

After experimenting for a while and writing some BadUSB Ducky scripts on Flipper Zero, I felt a bit overwhelmed by the [workflow](https://docs.flipper.net/zero/bad-usb) every time I wanted to test a change in the script.
I've been searching and testing some other solutions but I found lot of issues related with Linux graphical environment permissions and I decided to write something simple to test and write my FlipperZero's DuckyScripts.


## Usage

`$ git clone https://github.com/carvilsi/flipper0-badUSB-linux-tester`

`$ cd flipper0-badUSB-linux-tester`

`$ chmod a+x flipper0badusb_test`


```
Usage:

    $ ./flipper0badusb_test <flipper_ducky_script_file.txt> <out_file.sh> [test | silence]


If "test" is provided will run the DuckyScript after parsing it to ydotool.
If "silence" is provided will generate ydotool file without print to stdout. "Silence is goldenn" mode.
```

The you can test your FlipperZero's DuckyScript with:

`$ sh out_file.sh`

Or pass "test" after the command line and it will be executed after creating the sh file.

`$ ./flipper0badusb_test.py examples/hello-world.txt out.sh test`

### Dependencies
Depends on [ydotool](https://github.com/ReimuNotMoe/ydotool) for command-line automation tool on Linux. 

#### ArchLinux
- Install it: `$ sudo pacman -S ydotool`

- Run the service: `$ systemctl --user start ydotool`

#### Ubuntu (24.04 noble)
- Install it: `$ sudo apt install -y ydotool`

- Run the service: `$ systemctl --user start ydotool`

Note: had some inssues install it it from Ubuntu current package, but [build it from source](https://github.com/ReimuNotMoe/ydotool?tab=readme-ov-file#build) and install it worked for me.

## Tests

The test are very simple, just comparing the expected ydotool output with the provided DockyScript.

Tu run it: 

`$ sh tests/test.sh`

## Current Flipper's DuckyScript implemented commands

| Implemented |
|-------------|
|DEFAULT_DELAY|
|DEFAULTDELAY|
|STRINGLN|
|STRING|
|DELAY|
|ENTER|
|ALT|
|GUI|
|REM|
|ESC|
|F2|
|ID|

More info about Flipper's [BadUSB File Format](https://developer.flipper.net/flipperzero/doxygen/badusb_file_format.html)

---

⚠️ ADVISORY: This script should be used for authorized penetration testing and/or educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own computers and/or with the computer owner's permission.

---

Feedback from usage and contributions are very welcome.
Also if you like it, please leave a :star: I would appreciate it ;)


