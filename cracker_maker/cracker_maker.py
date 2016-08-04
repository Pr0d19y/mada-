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
    def __init__(self, grinder_pin, water_pin, button_pin, kneading_power_pin, kneading_pin, kneading_extrution_pin, baking_pin, quit_pin):
        self.logger = logging.getLogger(__name__)
        self.logger.info('starting cracker maker')

        self.logger.info('grinder_pin: {}'.format(grinder_pin))
        self.logger.info('water_pin: {}'.format(water_pin))
        self.logger.info('kneading_power_pin: {}'.format(kneading_power_pin))
        self.logger.info('kneading_pin: {}'.format(kneading_pin))
        self.logger.info('kneading_extrution_pin: {}'.format(kneading_extrution_pin))
        self.logger.info('button_pin: {}'.format(button_pin))
        self.logger.info('baking_pin: {}'.format(baking_pin))
        self.logger.info('quit_pin: {}'.format(quit_pin))
        self.print_cfg()

        self.grinder_pin = grinder_pin
        self.water_pin = water_pin
        self.kneading_power_pin = kneading_power_pin
        self.kneading_pin = kneading_pin
        self.kneading_extrution_pin = kneading_extrution_pin
        self.button_pin = button_pin
        self.baking_pin = baking_pin
        self.quit_pin = quit_pin

        self.running = True

        GPIO.setmode(GPIO.BCM)  # use chip numbering

        GPIO.setup(grinder_pin, GPIO.OUT)
        GPIO.setup(water_pin, GPIO.OUT)
        GPIO.setup(kneading_power_pin, GPIO.OUT)
        GPIO.setup(kneading_pin, GPIO.OUT)
        GPIO.setup(kneading_extrution_pin, GPIO.OUT)
        GPIO.setup(baking_pin, GPIO.OUT)
        GPIO.setup(quit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if cfg.USE_INPUT_BUTTON:
            self.logger.info('running in manual mode, use button to tart machine')
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            self.button_reader_thread = threading.Thread(target=self.button_reader)
            self.button_reader_thread.start()
        else:
            self.logger.info('running in auto mode')
            self.auto_runner = threading.Thread(target=self.auto_runner)
            self.auto_runner.start()
    
    def auto_runner(self):
        for i in range(16):
            if not self.running:
                return
            try:
                self.main_loop()
                if cfg.RUN_ONCE:
                    self.quit()
            except Exception as ex:
                self.logger.error('got exception: {}, probably quiting'.format(ex))
            sleep(1)
        self.logger.info('auto runner thread finished')

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
        self.logger.info('starting power for kneading machine')
        GPIO.output(self.kneading_power_pin, 1)
        sleep(2)
        
        self.knead()

        t_start_kneed = time()
        self.insert_water()

        #self.bake()
        kneeding_waiting_time = cfg.KNEADING_TIME - (time() - t_start_kneed)
        self.logger.info('waiting more {} [S] so kneading machine will finish auto kneeding'.format(kneeding_waiting_time))
        sleep(kneeding_waiting_time)
   	
	    if cfg.USE_PULSED_EXTRUSTION:
                self.small_extrusions()
            else:
                self.extrude()
        
        self.logger.info('stopping power to kneading machine')
        GPIO.output(self.kneading_power_pin, 0)
        sleep(TIME_TO_WAIT_BETWEEN_RUNS)
    
    def check_quit_pin(self):
        self.logger.info('in check quit pin')
        quit_state = GPIO.input(self.quit_pin)
        self.logger.info('quit state: {}'.format(quit_state))
        if not quit_state:
            self.logger.info('quit_state =0, calling quit function')
            self.quit()
        
    def grind_wheat(self):
        self.logger.info('in wheat grinder')
        if cfg.PULSE_GRINDER_FOR_STARTUP:
            self.logger.info('for startup, pulse grinder 3 times')
            for i in range(3):
                GPIO.output(self.grinder_pin, 1)
                sleep(0.2)
                GPIO.output(self.grinder_pin, 0)
                sleep(0.4)

        GPIO.output(self.grinder_pin, 1)
        sleep(cfg.GRINDING_TIME)
        GPIO.output(self.grinder_pin, 0)
        self.logger.info('finished grinding')

    def insert_water(self):
        self.logger.info('in insert_water, total time: {}'.format(cfg.WATER_POUR_TIME))
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
        self.logger.info('in knead')
        self.logger.debug('starting automatik kneading + extrusion')
        GPIO.output(self.kneading_pin, 1)
        sleep(0.5)
        GPIO.output(self.kneading_pin, 0)

        self.logger.info('finished knead function')

    def extrude(self):
        self.logger.info('in extrude, running {} times'.format(cfg.FULL_EXTRUSIONS_NUMBER))
        sleep(10)
        for i in range(cfg.FULL_EXTRUSIONS_NUMBER):
            GPIO.output(self.kneading_extrution_pin, 1)
            sleep(0.5)
            GPIO.output(self.kneading_extrution_pin, 0)
            self.logger.info('finished pushing kneading_extrution_pin')
            sleep(cfg.EXTRUSION_TIME + 10)
        self.logger.info('finished extrude')
    
    def small_extrusions(self):
	    self.logger.info('in small_extrusions')
            for i in range(cfg.AMOUNT_OF_PULSED_EXTRUSIONS):
                self.logger.info('starting extrusion {}'.format(i+1))
                self.one_pulsed_extrusion()
                self.logger.info('waiting {} seconds'.format(cfg.WAIT_TIME_AFTER_PULSED_EXTRUSION))
                sleep(cfg.WAIT_TIME_AFTER_PULSED_EXTRUSION)

    def one_pulsed_extrusion(self):
        self.logger.info('in oone_pulsed_extrusion')
        self.logger.debug('setting kneading_extrution_pin to 1')
        GPIO.output(self.kneading_extrution_pin, 1)
        sleep(0.5)
        self.logger.debug('setting kneading_extrution_pin to 0')
        GPIO.output(self.kneading_extrution_pin, 0)        
        sleep(cfg.PULSED_EXTRUSION_TIME)

        self.logger.debug('setting kneading_pin to 1')
        GPIO.output(self.kneading_pin, 1)
        sleep(0.5)
        self.logger.debug('setting kneading_pin to 0')
        GPIO.output(self.kneading_pin, 0)
        self.logger.info('one_pulsed_extrusion ended')

    def quit(self):
        self.logger.info('in quit, setting self.running to False')
        self.running = False
        sleep(0.1)
        GPIO.cleanup()

    def print_cfg(self):
	    with open('cracker_maker_config.py', 'r') as f:
                text_list = f.readlines()
	        full_text = ''
                for t in text_list:
                    full_text += t
                self.logger.info('current configuration file: \n {}'.format(full_text))

def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'cracker_maker_{}.log'
        .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_logging()
    grinder_pin = 24
    water_pin = 18
    button_pin = 7
    kneading_power_pin = 23
    kneading_pin = 15
    kneading_extrution_pin = 14
    baking_pin = 25
    quit_pin = 12
    baker = cracker_maker_controller(grinder_pin=grinder_pin, 
                                     water_pin=water_pin, 
                                     button_pin=button_pin, 
                                     kneading_power_pin=kneading_power_pin,
                                     kneading_pin=kneading_pin,
                                     kneading_extrution_pin=kneading_extrution_pin,
                                     baking_pin=baking_pin,
                                     quit_pin=quit_pin)

    #q = raw_input("Do you want to exit? (Y)")
    #if q is 'Y':
    #    baker.quit()
