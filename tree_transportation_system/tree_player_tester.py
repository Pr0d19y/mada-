__author__ = 'netanel'

import os
import RPi.GPIO as GPIO
import time
import datetime
import logging
from random import random


def start_test(gpio, test_time):
    logger = logging.getLogger('tree_player_tester')
    logger.info('starting tester at: {}'.format(datetime.datetime.now()))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)
    state = 1
    GPIO.output(gpio, 1)
    t0 = tc = time.time()

    while tc - t0 < test_time:
        time_to_sleep = random() * 10
        logger.info('waiting {} seconds'.format(time_to_sleep))
        time.sleep(time_to_sleep)
        new_state = not state
        logger.info('writing new state: {}'.format(new_state))
        GPIO.output(gpio, new_state)
        state = new_state
        tc = time.time()


def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'tree_player_tester_{}.log'
        .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    gpio = 23
    test_time = 60 * 60 * 24 * 6
    init_logging()
    start_test(gpio=gpio, test_time=test_time)