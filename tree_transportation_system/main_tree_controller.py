__author__ = 'netanel'

import logging
from collections import defaultdict
import random
#import RPi.GPIO as GPIO
#import pigpio
import os
import datetime
from time import sleep
import threading
import tree_controller_config as cfg
import sys
sys.path.append('../classes/')
import ip_reservations


class main_tree_controller(object):
    """
    'Big Tree display' controller
    inputs:
        - buttons_dict, dictionary of button_name, gpio
    outputs:
        - servos_dict, dictionary of servo_name, gpio - control servos
        - dc_motors_dict, dictionary of motor_name, gpio - control DC motors
        - tree_players_dict, dictionary of player_name, gpio - control other raspberry pi players
    """
    def __init__(self, servos_dict, dc_motors_dict, tree_players_dict, buttons_dict, simulated=False):
        self.logger = logging.getLogger(__name__)
        self.logger.info('starting main tree controller')

        self.logger.info('servos_dict: {}'.format(servos_dict))
        self.logger.info('dc_motors_dict: {}'.format(dc_motors_dict))
        self.logger.info('tree_players_dict: {}'.format(tree_players_dict))
        self.logger.info('buttons_dict: {}'.format(buttons_dict))
        self.logger.info('simulated: {}'.format(simulated))

        self.servos_dict = servos_dict
        self.dc_motors_dict = dc_motors_dict
        self.tree_players_dict = tree_players_dict
        self.buttons_dict = buttons_dict
        self.running = True
        self.current_state = None
        self.simulated = simulated
        self.statistics_counter = StatisticsCounter(statistics_interval_sec=1, filename=os.path.join('logs', 'main_tree_controller_statistics_{}.log'
            .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

        if not self.simulated:
            import RPi.GPIO as GPIO
            import pigpio
            self.my_pigpio = pigpio.pi()
            GPIO.setmode(GPIO.BCM)  # use chip numbering

            for button_name, pin_number in self.buttons_dict.iteritems():
                self.logger.info('setting up button: {}'.format(button_name))
                GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                #GPIO.add_event_detect(pin_number, GPIO.BOTH, callback=self.event, bouncetime=250)

            for player_name, pin_number in self.tree_players_dict.iteritems():
                self.logger.info('setting up player: {}'.format(player_name))
                GPIO.setup(pin_number, GPIO.OUT)

            for dc_motor_name, pin_number in self.dc_motors_dict.iteritems():
                self.logger.info('setting up dc motor: {}'.format(dc_motor_name))
                self.my_pigpio.set_mode(pin_number, pigpio.OUTPUT)
                self.my_pigpio.set_PWM_frequency(pin_number, cfg.DC_MOTOR_PWM_FREQUENCY)

            for servo_motor_name, pin_number in self.servos_dict.iteritems():
                self.logger.info('setting up servo motor: {}'.format(servo_motor_name))
                self.my_pigpio.set_mode(pin_number, pigpio.OUTPUT)

        self.button_reader_thread = threading.Thread(target=self.button_reader)
        self.button_reader_thread.start()

    def button_reader(self):
        self.logger.info('button_reader started')
        while self.running:
            current_state = self.read_current_buttons_state()
            if current_state != self.current_state:
                try:
                    for k, new_v, old_v in zip(current_state.keys(), current_state.values(), self.current_state.values()):
                        self.statistics_counter.add_counter('{} {}'.format(k, new_v))
                except Exception as ex:
                    print current_state
                    print self.current_state
                    print ex

                self.current_state = current_state
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
        current_state = self.current_state

        if current_state['button1_water'] == 1:
            self.logger.debug('demo, if water = HIGH, move first servo and signal HIGH for first player')
            self.servo_gradual_movement(pin=self.servos_dict['leaf2'], current_duty=cfg.SERVO_MINIMAL_POSITION, target_duty=cfg.SERVO_MAXIMAL_POSITION)
            if not self.simulated:
                GPIO.output(self.tree_players_dict['player1'], 1)
            self.dc_motor_mover(pin=self.dc_motors_dict['water'], duty=cfg.DC_MOTOR_MAXIMAL_DUTYCYCLE)

        else:
            self.logger.debug('demo, if water = LOW, move first servo and signal HIGH for first player')
            self.servo_gradual_movement(pin=self.servos_dict['leaf2'], current_duty=cfg.SERVO_MAXIMAL_POSITION, target_duty=cfg.SERVO_MINIMAL_POSITION)
            if not self.simulated:
                GPIO.output(self.tree_players_dict['player1'], 0)
            self.dc_motor_mover(pin=self.dc_motors_dict['water'], duty=cfg.DC_MOTOR_MINIMAL_DUTYCYCLE)

    def servo_gradual_movement(self, pin, current_duty, target_duty):
        """
        move a servo in a few legs to get a slower movement
        :param pin:
        :param current_duty:
        :param target_duty:
        :return:
        """
        self.logger.debug('gradual movement started, pin: {}, current duty: {}, target duty: {}'.format(pin, current_duty, target_duty))

        if current_duty < target_duty:
            delta = cfg.SERVO_GRADUAL_MOVEMENT_STEP
        else:
            delta = 0 - cfg.SERVO_GRADUAL_MOVEMENT_STEP

        for step in range(current_duty, target_duty + delta, delta):
            self.servo_mover(pin=pin, duty=step)
            sleep(cfg.SERVO_GRADUAL_MOVEMENT_DELAY)

        self.servo_mover(pin=pin, duty=0)
        self.logger.debug('gradual movement ended')

    def dc_motor_mover(self, pin, duty):
        """
        change duty cycle of one dc motor to move it to a new position
        :param pin: servo GPIO
        :param duty: new duty cycle
        :return:
        """
        if self.simulated:
            return
        self.my_pigpio.set_PWM_dutycycle(pin, duty)

    def servo_mover(self, pin, duty):
        """
        change duty cycle of one servo motor to move it to a new position
        :param pin: servo GPIO
        :param duty: new duty cycle
        :return:
        """
        if self.simulated:
            return
        self.my_pigpio.set_servo_pulsewidth(pin, duty)

    def read_current_buttons_state(self):
        """
        read all buttons states
        :return: a dictionary of {button_name: state}
        """
        state = {}
        for button_name, pin_number in self.buttons_dict.iteritems():
            if self.simulated:
                st = random.randint(0, 2)
            else:
                st = GPIO.input(pin_number)
            state[button_name] = st

        return state

    def quit(self):
        self.running = False
        for dc_motor_name, pin_number in self.dc_motors_dict.iteritems():
            self.logger.info('stopping dc motor: {}'.format(dc_motor_name))
            self.my_pigpio.set_PWM_dutycycle(pin_number, 0)

        for servo_motor_name, pin_number in self.servos_dict.iteritems():
            self.logger.info('stopping servo motor: {}'.format(servo_motor_name))
            self.my_pigpio.set_servo_pulsewidth(pin_number, 0)

        sleep(0.01)
        GPIO.cleanup()
        self.my_pigpio.stop()


class StatisticsCounter(threading.Thread):
    """
    """
    def __init__(self, statistics_interval_sec, filename):
        self.output = open(name=filename, mode='w+')
        self.statistics_interval_sec = datetime.timedelta(seconds=statistics_interval_sec)
        self.counters = defaultdict(int)
        self.last_statistics_time = datetime.datetime.now()
        self.running = True
        threading.Thread.__init__(self)
        threading.Thread.start(self)

    def run(self):
        print 'thresd start'
        while self.running:
            if datetime.datetime.now() - self.last_statistics_time > self.statistics_interval_sec:
                a = str(str(self.counters.__repr__()))
                print a
                self.output.write(a)
                self.last_statistics_time = datetime.datetime.now()
            sleep(1)

    def add_counter(self, c):
        self.counters[c] += 1

    def quit(self):
        self.running = False
        self.output.close()


def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'main_tree_controller_{}.log'
        .format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S'))))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_logging()
    logger = logging.getLogger()
    try:
        ip_reservations.set_static_ip(ip=ip_reservations.IPS['tree_controller'])
    except Exception as ex:
        logger.info('while trying to set static IP got exception: {}'.format(ex))

    servos_dict = {'leaf1': 22, 'leaf2': 4}
    dc_motors_dict = {'water': 5}
    tree_players_dict = {'player1': 8}
    buttons_dict = {'button1_water': 23, 'button2_sun': 10}

    player = main_tree_controller(servos_dict=servos_dict, dc_motors_dict=dc_motors_dict,
                                  tree_players_dict=tree_players_dict, buttons_dict=buttons_dict, simulated=True)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
