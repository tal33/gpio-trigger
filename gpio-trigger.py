#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import RPi.GPIO as GPIO
import urllib.request
import subprocess
import threading
import queue
import statusled
from statusled.statusled import setColor



def execute_curl(url: str):
    urllib.request.urlopen(url)


def execute_command(command: str):
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


def execute_action(trigger_queue: queue.Queue, rgb_color: statusled.RgbColor, action_function: callable, action_param: str):
    while True:
        trigger_queue.get()
        setColor(rgb_color)
        action_function(action_param)


ACTION_FUNCTIONS = {
    "curl": execute_curl,
    "command": execute_command
}


if __name__ == '__main__':
    board_pin = int(sys.argv[1])
    rgb_color = statusled.RgbColor[sys.argv[2].upper()]
    action_type = sys.argv[3]
    action = sys.argv[4]

    if action_type not in ACTION_FUNCTIONS:
        print("No such action type", action_type, file=sys.stderr)
        exit(1)

    event_queue = queue.Queue()
    threading.Thread(target=execute_action, args=(event_queue, rgb_color, ACTION_FUNCTIONS[action_type], action), daemon=True).start()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(board_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #
    # bouncetime
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    #
    while True:
        GPIO.wait_for_edge(board_pin, GPIO.FALLING, bouncetime=200)
        event_queue.put(1, False)

