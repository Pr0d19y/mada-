__author__ = 'nfreiman'
import logging


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