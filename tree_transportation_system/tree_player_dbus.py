__author__ = 'netanel'

import threading
import logging
import datetime
import os
#from classes import omxplayer
import RPi.GPIO as GPIO
from time import sleep
from omxplayer import OMXPlayer


class tree_player(object):
    """
    control one screen on the "Big Tree display"
    toggle between two different movies according to GPIO input signal
    """

    def __init__(self, gpio_number, movie_1, movie_2):
        self.logger = logging.getLogger('tree_player')
        self.logger.info('starting player')
        self.logger.info('movie 1: {}'.format(movie_1))
        self.logger.info('movie 2: {}'.format(movie_2))
        self.logger.info('GPIO: {} (BCM)'.format(gpio_number))

        self.stop_gpio = 21
        self.logger.info('stop GPIO: {} (BCM)'.format(self.stop_gpio))
        self.control_gpio = gpio_number
        self.movie_1 = movie_1
        self.movie_2 = movie_2
        self.current_state = None
        self.polling_tries = 0
        self.stop_state = 0
        self.stop_tries = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.stop_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(self.control_gpio, GPIO.BOTH, callback=self.event, bouncetime=300)
        #GPIO.add_event_detect(self.stop_gpio, GPIO.FALLING, callback=self.quit, bouncetime=200)

        #self.movie_1_controller = omxplayer.OMXPlayer(mediafile=self.movie_1, args=r'--loop -b --no-osd', start_playback=False)
        #self.movie_2_controller = omxplayer.OMXPlayer(mediafile=self.movie_2, args=r'--loop -b --no-osd', start_playback=False)

        self.movie_1_controller = OMXPlayer(filename=self.movie_1, args=['--loop', '-b', '--no-osd'])
        self.movie_2_controller = OMXPlayer(filename=self.movie_2, args=['--loop', '-b', '--no-osd'])
        sleep(1)
        self.running = True
        self.button_reader_thread = threading.Thread(target=self.button_reader)
        self.button_reader_thread.start()

    def button_reader(self):
        self.logger.info('button_reader started')
        while self.running:
            current_state = self.read_current_buttons_state()
            if current_state != self.current_state and self.polling_tries == 20:
                self.current_state = current_state
                self.main_loop()
            elif current_state != self.current_state and self.polling_tries < 20:
                self.polling_tries += 1
            else:
                self.polling_tries = 1

            stop_state = not GPIO.input(self.stop_gpio) 
            if stop_state and self.stop_tries == 50:
                self.quit()
            elif stop_state and self.stop_tries < 50:
                self.stop_tries += 1
            else:
                self.stop_tries = 1

            sleep(0.005)

        self.logger.info('button_reader ended')

    def read_current_buttons_state(self):
        """
        read control_gpio state
        """
        return GPIO.input(self.control_gpio)

    def main_loop(self):
        """
        one iteration of main loop,
        called when input is changed,
        stop one movie, seek to 0 (so next time we start from beginning) and play other movie
        :return:
        """
        current_state = self.current_state
        if current_state:
            self.logger.info('state changed to HIGH, show BAD fruit movie')
            self.movie_2_controller.pause()
            sleep(0.1)
            self.movie_2_controller.set_position(0)
            sleep(0.1)
            self.movie_1_controller.play()

        else:
            self.logger.info('state changed to LOW, show GOOD fruit movie')
            self.movie_1_controller.pause()
            sleep(0.1)
            self.movie_1_controller.set_position(0)
            sleep(0.1)
            self.movie_2_controller.play()
        sleep(0.3)

    def quit(self):
        self.logger.info('in quit()')
        self.running = False
        sleep(0.1)
        GPIO.cleanup()
        self.logger.info('stopping both movies')
        self.movie_1_controller.stop()
        self.movie_2_controller.stop()
        sleep(0.5)
        self.logger.info('closing both players')
        try:
            self.movie_1_controller.quit()
        except Exception as ex:
            self.logger.error('while closing player 1, got ex: {}'.format(ex))

        try:
            self.movie_2_controller.quit()
        except Exception as ex:
            self.logger.error('while closing player 2, got ex: {}'.format(ex))

        sleep(0.5)
        self.logger.info('quit function ended')


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
    movie1 = r'fruit_bad_720.mp4'
    movie2 = r'fruit_good_720.mp4'
    #movie2 = r'piyoni_day_720px.mp4'
    #movie1 = r'piyoni_night_720px.mp4'
    gpio = 22
    player = tree_player(gpio_number=gpio, movie_1=movie1, movie_2=movie2)

    #q = raw_input("Do you want to exit? (Y)")
    #if q is 'Y':
    #    player.quit(None)
