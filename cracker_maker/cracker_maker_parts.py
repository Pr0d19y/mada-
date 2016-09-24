__author__ = 'nfreiman'
import logging
from time import sleep, time
import threading
from datetime import datetime


class Grinder(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.grinding_state = None

    def start_grinding(self):
        self.logger.info('in Grinder.start_grinding')
        if not self.grinding_state:
            self.grinding_state = True
            # implement start of grinder
        else:
            self.logger.info('grinder already ON, doing nothing')

    def stop_grinding(self):
        self.logger.info('in Grinder.stop_grinding')
        if self.grinding_state:
            self.grinding_state = False
            # implement stop of grinder
        else:
            self.logger.info('grinder already OFF, doing nothing')


class Water(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.water_state = None

    def start_water(self):
        self.logger.info('in Water.start_water')
        if not self.water_state:
            self.water_state = True
            # implement start of grinder
        else:
            self.logger.info('Water already ON, doing nothing')

    def stop_water(self):
        self.logger.info('in Water.stop_water')
        if self.water_state:
            self.water_state = False
            # implement stop of grinder
        else:
            self.logger.info('Water already OFF, doing nothing')


class Kneader(object):
    def __init__(self, button_1, button_2):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.states = {'OFF': 0, 'KNEADING': 1, 'EXTRUDING': 2}
        self.kneader_state = self.states['OFF']
        self.button_1 = button_1
        self.button_2 = button_2
        self.logger.info('created Kneader object, Button_1: {}, Button_2: {}, state: {}'.format(self.button_1,
                                                                                                self.button_2,
                                                                                                self.state_to_str(self.kneader_state)))
        self.operation_timer = ''

    def start_kneading_cycle(self):
        self.logger.info('in Kneader.start_kneading_cycle')
        if self.kneader_state == self.states['OFF']:
            self.kneader_state = self.states['KNEADING']
            t = threading.Thread(target=self.kneader_thread_func, args=(20,))
            t.setDaemon(True)
            t.start()

    def extrude(self):
        self.logger.info('in Kneader.small_extrude')
        if self.kneader_state == self.states['OFF']:
            self.kneader_state = self.states['EXTRUDING']
            t = threading.Thread(target=self.extruder_thread_func, args=(5,))
            t.setDaemon(True)
            t.start()

    def extruder_thread_func(self, extrude_time):
        self.logger.info('in Kneader.extruder_thread_func')
        #TODO:  actual button changing
        sleep(extrude_time)
        self.kneader_state = self.states['OFF']

    def kneader_thread_func(self, knead_time):
        self.logger.info('in Kneader.kneader_thread_func')
        t0 = tc = datetime.now()
        #TODO:  actual button changing
        while (tc - t0).total_seconds() < knead_time:
            sleep(0.05)
            self.operation_timer = knead_time - (t0 - datetime.now())

        self.kneader_state = self.states['OFF']

    def state_to_str(self, state):
        for k, v in self.states.iteritems():
            if v == state:
                return k
