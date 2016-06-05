__author__ = 'netanel'

import logging
import datetime
import os
from classes import omxplayer
import RPi.GPIO as GPIO
import time


class tree_player(object):
    """
    control one screen on the "Big Tree display"
    toggle between two different movies according to GPIO input signal
    """

    def __init__(self, gpio_number, movie_1, movie_2):
        self.logger = logging.getLogger(__name__)
        self.logger.info('starting player')
        self.logger.info('movie 1: {}'.format(movie_1))
        self.logger.info('movie 2: {}'.format(movie_2))
        self.logger.info('GPIO: {} (BCM)'.format(gpio_number))

        self.control_gpio = gpio_number
        self.movie_1 = movie_1
        self.movie_2 = movie_2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.control_gpio, GPIO.BOTH, callback=self.event, bouncetime=300)

        self.movie_1_controller = omxplayer.OMXPlayer(mediafile=self.movie_1, args='--loop')
        time.sleep(0.5)
        self.movie_1_controller.toggle_pause()
        self.movie_2_controller = omxplayer.OMXPlayer(mediafile=self.movie_2, args='--loop', start_playback=True)
        time.sleep(0.5)

    def event(self, channel):
        current_state = GPIO.input(self.control_gpio)
        if current_state:
            self.logger.info('event detected, ch: {}, RISING event'.format(channel))
            self.logger.info('toggling pause for two movies'.format(channel))
            self.movie_2_controller.toggle_pause()
            self.movie_1_controller.toggle_pause()
        else:
            self.logger.info('event detected, ch: {}, FALLING event'.format(channel))
            self.logger.info('doing nothing'.format(channel))
            #self.movie_2_controller.toggle_pause()
            #self.movie_1_controller.toggle_pause()

    def quit(self):
        GPIO.cleanup()
        self.movie_1_controller.stop()
        self.movie_2_controller.stop()

def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'tree_player_{}.log'
        .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    init_logging()
    movie1 = r'tomato_blink_sequence.mp4'
    movie2 = r'tzaleket_blink.mp4'
    gpio = 22
    player = tree_player(gpio_number=gpio, movie_1=movie1, movie_2=movie2)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
