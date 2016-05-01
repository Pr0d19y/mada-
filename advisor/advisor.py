__author__ = 'Or Levi'

#import movie_player
import advisor_config as config
import time
import RPi.GPIO as GPIO


class advisor(object):
    """
    controls one advisor screen.
    activates the advisor video according to GPIO input.
    """

    def __init__(self, gpio_number, movie):
        print 'starting player'
        print 'movie: {}'.format(movie)
        print 'GPIO: {}'.format(gpio_number)

        self.control_gpio = gpio_number
        self.movie = movie
        self.last_rise_time = time.time()
        self.last_fall_time = time.time()

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.control_gpio, GPIO.BOTH, callback=self.event, bouncetime=50)

    def event(self, channel):
        current_state = GPIO.input(self.control_gpio)
        if current_state:
            print 'event detected, ch: {}, RISING event'.format(channel)
            self.last_rise_time = time.time()
            #self.movie_controller.play()
        else:
            print 'event detected, ch: {}, FALLING event'.format(channel)
            self.last_fall_time = time.time()
            #self.movie_controller.stop()

    def quit(self):
        GPIO.cleanup()


if __name__ == '__main__':
    movie = r'path/to/movie'
    gpio = 22
    player = advisor(gpio_number=gpio, movie=movie)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
