__author__ = 'netanel'

import logging
import RPi.GPIO as GPIO
import os
import datetime
from time import sleep, time
import threading
import cracker_maker_config as cfg


class cracker_maker_controller(object):
    """
    """
    def __init__(self, grinder_pin, water_pin, button_pin, kneading_pin,kneading_extrution_pin, baking_pin, quit_pin):
        self.logger = logging.getLogger(__name__)
        self.logger.info('starting cracker maker')

        self.logger.info('grinder_pin: {}'.format(grinder_pin))
        self.logger.info('water_pin: {}'.format(water_pin))
        self.logger.info('kneading_pin: {}'.format(kneading_pin))
        self.logger.info('kneading_extrution_pin: {}'.format(kneading_extrution_pin))
        self.logger.info('button_pin: {}'.format(button_pin))
        self.logger.info('baking_pin: {}'.format(baking_pin))
        self.logger.info('quit_pin: {}'.format(quit_pin))

        self.grinder_pin = grinder_pin
        self.water_pin = water_pin
        self.kneading_pin = kneading_pin
        self.kneading_extrution_pin = kneading_extrution_pin
        self.button_pin = button_pin
        self.baking_pin = baking_pin
        self.quit_pin = quit_pin

        self.running = True

        GPIO.setmode(GPIO.BCM)  # use chip numbering
        GPIO.setup(grinder_pin, GPIO.OUT)
        GPIO.setup(water_pin, GPIO.OUT)
        GPIO.setup(kneading_pin, GPIO.OUT)
        GPIO.setup(kneading_extrution_pin, GPIO.OUT)
        GPIO.setup(baking_pin, GPIO.OUT)
        GPIO.setup(quit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if cfg.USE_INPUT_BUTTON:
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self.button_reader_thread = threading.Thread(target=self.button_reader)
            self.button_reader_thread.start()
        else:
            self.auto_runner = threading.Thread(target=self.auto_runner)
            self.auto_runner.start()
    
    def auto_runner(self):
        for i in range(16):
            try:
                self.main_loop()
                if cfg.RUN_ONCE:
                    self.quit()
            except Exception as ex:
                self.logger.info('got exception: {}, probably quiting'.format(ex))
            sleep(1)

    def button_reader(self):
        self.logger.info('button_reader started')
        while self.running:
            current_state = GPIO.input(self.button_pin)
            if current_state == 1:
                self.main_loop()
            sleep(0.005)
        self.logger.info('button_reader ended')

    def main_loop(self):
        """
        one iteration of main loop,
        called when input is changed,
        define logic and change tree motors, movies etc.
        :return:
        """
        self.logger.info('starting main loop')
        
        self.check_quit_pin()
        self.grind_wheat()
        #self.insert_water()
        self.knead()
        t_start_kneed = time()
        self.insert_water()
        #self.bake()
        sleep(cfg.KNEADING_TIME - (time() - t_start_kneed))
        
        self.extrude()
        #sleep(TIME_TO_WAIT_BETWEEN_RUNS)
    
    def check_quit_pin(self):
        self.logger.info('in check quit pin')
        quit_state = GPIO.input(self.quit_pin)
        self.logger.info('quit state: {}'.format(quit_state))
        if not quit_state:
            self.logger.info('quit_state =0, calling quit function')
            self.quit()
        
    def grind_wheat(self):
        self.logger.info('in wheat grinder')
        GPIO.output(self.grinder_pin, 1)
        sleep(cfg.GRINDING_TIME)
        GPIO.output(self.grinder_pin, 0)
        self.logger.info('finished grinding')

    def insert_water(self):
        self.logger.info('in water pourer, total time: {}'.format(cfg.WATER_POUR_TIME))
        for i in range(cfg.WATER_POUR_SEGMENTS):
            self.logger.info('starting pour no {}'.format(i))    
            GPIO.output(self.water_pin, 1)
            self.logger.info('pouring: {} [S]'.format(cfg.WATER_POUR_TIME / cfg.WATER_POUR_SEGMENTS))
            sleep(cfg.WATER_POUR_TIME / cfg.WATER_POUR_SEGMENTS)
            self.logger.info('stoping pour no {}'.format(i))
            GPIO.output(self.water_pin, 0)
            sleep(cfg.WATER_DELAY_BETWEEN_SEGMENT)
        self.logger.info('finished pouring water')

    def bake(self):
        self.logger.info('in baker')
        GPIO.output(self.baking_pin, 1)
        sleep(cfg.BAKING_TIME)
        GPIO.output(self.baking_pin, 0)
        self.logger.info('finished baking')

    def knead(self):
        self.logger.info('in kneader')
        GPIO.output(self.kneading_pin, 1)
        sleep(0.5)
        GPIO.output(self.kneading_pin, 0)
        self.logger.info('finished pushing kneading pin')
        #sleep(cfg.KNEADING_TIME)
        self.logger.info('finished kneading')

    def extrude(self):
        self.logger.info('in extruder, running {} times'.format(cfg.EXTRUSION_NEMBER))
        sleep(10)
        for i in range(cfg.EXTRUSION_NEMBER):
            GPIO.output(self.kneading_extrution_pin, 1)
            sleep(0.5)
            GPIO.output(self.kneading_extrution_pin, 0)
            self.logger.info('finished pushing kneading_extrution_pin')
            sleep(cfg.EXTRUSION_TIME + 10)
        self.logger.info('finished extruder')
        
    def quit(self):
        self.running = False
        sleep(0.1)
        GPIO.cleanup()


def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'cracker_baker_{}.log'
        .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_logging()
    grinder_pin = 5
    water_pin = 15
    button_pin = 21
    kneading_pin = 27
    kneading_extrution_pin = 21
    baking_pin = 13
    quit_pin = 7
    baker = cracker_maker_controller(grinder_pin=grinder_pin, 
                                     water_pin=water_pin, 
                                     button_pin=button_pin, 
                                     kneading_pin=kneading_pin,
                                     kneading_extrution_pin=kneading_extrution_pin,
                                     baking_pin=baking_pin,
                                     quit_pin=quit_pin)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        baker.quit()
