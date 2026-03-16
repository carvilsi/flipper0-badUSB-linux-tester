#!/usr/bin/env python3

import os
import re
import sys
import argparse

YDTL = "ydotool"
INPUT_EVENT_CODES_H = "/usr/include/linux/input-event-codes.h"

default_delay = None


def get_input_event_code_key(char_key):
    with open(INPUT_EVENT_CODES_H, "r") as f:
        header_file = f.read()
        match = re.search(
            rf"#define KEY_{char_key.upper()}\s+\d+", header_file, re.MULTILINE
        )
        if match:
            return match.group().replace("\t", " ").split(" ")[-1]
        else:
            raise Exception("input event key code not found")


class DuckyScriptCommands:
    # Commands from DuckyScript to this
    DEFAULT_DELAY = "DEFAULT_DELAY"
    DEFAULTDELAY = "DEFAULTDELAY"
    STRINGLN = "STRINGLN"
    STRING = "STRING"
    DELAY = "DELAY"
    ENTER = "ENTER"
    GUI = "GUI"
    REM = "REM"
    ALT = "ALT"
    ESC = "ESC"
    F2 = "F2"
    ID = "ID"

    # definitions key names at /user/include/linux/input-event-codes.h
    ENTER_KEY = "ENTER"
    GUI_KEY = "LEFTMETA"
    ALT_KEY = "LEFTALT"
    ESC_KEY = "ESC"

    # helpers
    DELAY_SYMB = "sleep"
    REM_SYMB = "#"


def ydotool_key_press_release(key_char):
    key_code = get_input_event_code_key(key_char.strip())
    kpress = f"{key_code}:1"
    kreles = f"{key_code}:0"
    return (kpress, kreles)


def build_ydotool_command_key(key_char, extra_key_char=None):
    kpress, krelea = ydotool_key_press_release(key_char)
    command = f"{YDTL} key {kpress} {krelea}"
    if extra_key_char is not None:
        ext_kpress, ext_krelea = ydotool_key_press_release(extra_key_char)
        command = f"{YDTL} key {kpress} {ext_kpress} {ext_krelea} {krelea}"

    command += "\n"
    return command


def build_ydotool_command_type(string):
    return f"{YDTL} type '{string}'\n"


def format_delay(commands):
    value = float(int(commands[1:][0]) / 1000)
    return int(value) if value.is_integer() else value


def process_duckyscript_line(line, num, fos, silence=False):
    commands = line.replace("\n", "").split(" ")

    dcmd = None
    global default_delay

    match commands[0]:
        case DuckyScriptCommands.GUI:
            if len(commands) > 0:
                dcmd = build_ydotool_command_key(
                    DuckyScriptCommands.GUI_KEY, commands[1]
                )
            else:
                dcmd = build_ydotool_command_key(DuckyScriptCommands.GUI_KEY)

        case DuckyScriptCommands.REM:
            dcmd = f"{DuckyScriptCommands.REM_SYMB} {' '.join(commands[1:])}\n"

        case DuckyScriptCommands.STRING:
            dcmd = build_ydotool_command_type(" ".join(commands[1:]))

        case DuckyScriptCommands.STRINGLN:
            dcmd = build_ydotool_command_type(" ".join(commands[1:]))
            dcmd += build_ydotool_command_key(DuckyScriptCommands.ENTER_KEY)

        case DuckyScriptCommands.DELAY:
            dcmd = f"{DuckyScriptCommands.DELAY_SYMB} {format_delay(commands)}\n"

        case DuckyScriptCommands.DEFAULTDELAY | DuckyScriptCommands.DEFAULT_DELAY:
            default_delay = (
                f"{DuckyScriptCommands.DELAY_SYMB} {format_delay(commands)}\n"
            )

        case DuckyScriptCommands.ENTER:
            dcmd = build_ydotool_command_key(DuckyScriptCommands.ENTER_KEY)

        case DuckyScriptCommands.ALT:
            if len(commands) > 0:
                dcmd = build_ydotool_command_key(
                    DuckyScriptCommands.ALT_KEY, commands[1]
                )
            else:
                dcmd = build_ydotool_command_key(DuckyScriptCommands.ALT_KEY)

        case DuckyScriptCommands.ID:
            # nothing to do when defining a device ID, eg:
            # ID 1234:abcd Generic:USB Keyboard
            pass

        case DuckyScriptCommands.ESC:
            dcmd = build_ydotool_command_key(DuckyScriptCommands.ESC_KEY)

        case _:
            err_msg = f"Unknown or not implemented DuckyScript command: {commands[0]}"
            raise Exception(err_msg)

    if dcmd is not None:
        fos.write(dcmd)

    if default_delay is not None:
        fos.write(default_delay)

    if not silence:
        print(f"{num}: {line}")


def header():
    print("\n")
    print("▐▘▜ ▘        ▄▖▌    ▌    ▌   ▗     ▗ ")
    print("▜▘▐ ▌▛▌▛▌█▌▛▘▛▌▛▌▀▌▛▌▌▌▛▘▛▌  ▜▘█▌▛▘▜▘")
    print("▐ ▐▖▌▙▌▙▌▙▖▌ █▌▙▌█▌▙▌▙▌▄▌▙▌▄▖▐▖▙▖▄▌▐▖")
    print("     ▌ ▌                             ")
    print("with <3 by (#4|2\n\n")


def parse_cli():
    parser = argparse.ArgumentParser(
            description="Test your FlipperZero's DuckyScripts without uploading to device",
            epilog="With <3 by (#4|2; Only works on Linux; to get more info please check: https://github.com/carvilsi/flipper0-badUSB-linux-tester?tab=readme-ov-file#flipper0-badusb-linux-tester")
    parser.add_argument(
            "ducky_script",
            help="FlipperZero DuckyScript to test")
    parser.add_argument(
            "-o", "--out",
            help="Output filename; e.g my_out.sh; default out.sh")
    parser.add_argument(
            "-t", "--test",
            help="If we want to test after parsing the DuckyScript to ydotool format",
            action="store_true")
    parser.add_argument(
            "-s", "--silence",
            help="Silence is golden; no output to stdout",
            action="store_true")

    args = parser.parse_args()

    return args


def main():
    args = parse_cli()
    try:

        duckyscript = open(args.ducky_script, "r", encoding="UTF-8")

        fout = args.out if args.out is not None else "out.sh"
        ydotoolscript = open(fout, "w", encoding="UTF-8")

        ydotoolscript.write("#!/bin/bash\n\n")

        ydotoolscript.write(
            "# parsed onto ydotool commands by flipper0badusb_test with <3 by (#4|2\n"
        )
        ydotoolscript.write(
            "# https://github.com/carvilsi/flipper0-badUSB-linux-tester\n"
        )

        if not args.silence:
            header()
            print("Parsing...\n")

        command_num = 0
        for line in duckyscript:
            if len(line.strip()) > 0:
                process_duckyscript_line(line, command_num, ydotoolscript, args.silence)
                command_num += 1

        if not args.silence:
            print(f"Parsed {command_num} lines from {args.ducky_script} onto {fout}\n")

        duckyscript.close()
        ydotoolscript.close()

        if args.test:
            os.system(f"sh {fout}")

    except Exception as e:
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    main()

