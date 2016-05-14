__author__ = 'netanel'

import RPi.GPIO as GPIO
import pigpio


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
    def __init__(self, servos_dict, dc_motors_dict, tree_players_dict, buttons_dict):
        print 'starting main tree controller'

        print 'servos_dict: {}'.format(servos_dict)
        print 'dc_motors_dict: {}'.format(dc_motors_dict)
        print 'tree_players_dict: {}'.format(tree_players_dict)
        print 'buttons_dict: {}'.format(buttons_dict)

        self.servos_dict = servos_dict
        self.dc_motors_dict = dc_motors_dict
        self.tree_players_dict = tree_players_dict
        self.buttons_dict = buttons_dict
        self.my_pigpio = pigpio.pi()

        GPIO.setmode(GPIO.BCM)  # use chip numbering
        for button_name, pin_number in self.buttons_dict.iteritems():
            print('setting up button: {}'.format(button_name))
            GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin_number, GPIO.BOTH, callback=self.event, bouncetime=50)

        for player_name, pin_number in self.tree_players_dict.iteritems():
            print('setting up player: {}'.format(player_name))
            GPIO.setup(pin_number, GPIO.OUT)

        for dc_motor_name, pin_number in self.dc_motors_dict.iteritems():
            print('setting up dc motor: {}'.format(dc_motor_name))
            GPIO.setup(pin_number, GPIO.OUT)

        for servo_motor_name, pin_number in self.servos_dict.iteritems():
            print('setting up dc motor: {}'.format(dc_motor_name))
            self.my_pigpio.set_mode(pin_number, pigpio.OUTPUT)

    def event(self, channel):
        """
        called when some input has changed (callback function)
        - read all inputs
        - determine desired outputs
        - set outputs
        :param channel:
        :return:
        """
        current_state = self.read_current_buttons_state()

        '''
        here should be some logic that will determine the state of the servos,
        dc motors and players according to buttons state
        '''
        if current_state['button1_water'] == 1:
            print('demo, if water = HIGH, move first servo and signal HIGH for first player')
            self.servo_mover(pin=self.servos_dict['leaf1'], duty=2200)
            GPIO.output(self.tree_players_dict['player1'], 1)
        else:
            print('demo, if water = HIGH, move first servo and signal HIGH for first player')
            self.servo_mover(pin=self.servos_dict['leaf1'], duty=800)
            GPIO.output(self.tree_players_dict['player1'], 0)

    def servo_mover(self, pin, duty):
        """
        change duty cicle of one servo motor to move it to a new position
        :param pin: servo GPIO
        :param duty: new duty cicle
        :return:
        """
        print('changing servo on pin: {} to dc: {}'.format(pin, duty))
        self.my_pigpio.set_servo_pulsewidth(pin, duty)

    def read_current_buttons_state(self):
        """
        read all buttons states
        :return: a dictionary of {button_name: state}
        """
        print('in read_current_buttons_state')
        state = {}
        for button_name, pin_number in self.buttons_dict.iteritems():
            st = GPIO.input(pin_number)
            print('button: {}, pin: {}, state: {}'.format(button_name, pin_number, st))
            state[button_name] = st

        print('read state dict: {}'.format(state))
        return state

    def quit(self):
        GPIO.cleanup()
        self.my_pigpio.stop()


if __name__ == '__main__':
    servos_dict = {'leaf1': 22, 'leaf2': 4}
    dc_motors_dict = {'water': 5}
    tree_players_dict = {'player1': 8}
    buttons_dict = {'button1_water': 23, 'button2_sun': 10}

    player = main_tree_controller(servos_dict=servos_dict, dc_motors_dict=dc_motors_dict,
                                  tree_players_dict=tree_players_dict, buttons_dict=buttons_dict)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
