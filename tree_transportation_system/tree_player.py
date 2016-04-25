__author__ = 'netanel'

#import movie_player
import RPi.GPIO as GPIO


class tree_player(object):
    """
    control one screen on the "Big Tree display"
    toggle between two different movies according to GPIO input signal
    """

    def __init__(self, gpio_number, movie_1, movie_2):
        print 'starting player'
        print 'movie 1: {}'.format(movie_1)
        print 'movie 2: {}'.format(movie_2)
        print 'GPIO: {}'.format(gpio_number)

        self.control_gpio = gpio_number
        self.movie_1 = movie_1
        self.movie_2 = movie_2

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.control_gpio, GPIO.BOTH, callback=self.event, bouncetime=50)

        #self.movie_1_controller = movie_player.movie_player(movies_file=self.movie_1)
        #self.movie_2_controller = movie_player.movie_player(movies_file=self.movie_2)

    def event(self, channel):
        current_state = GPIO.input(self.control_gpio)
        if current_state:
            print 'event detected, ch: {}, RISING event'.format(channel)
            #self.movie_2_controller.stop()
            #self.movie_1_controller.play()
        else:
            print 'event detected, ch: {}, FALLING event'.format(channel)
            #self.movie_1_controller.stop()
            #self.movie_2_controller.play()

    def quit(self):
        GPIO.cleanup()


if __name__ == '__main__':
    movie1 = r'path/to/movie1'
    movie2 = r'path/to/movie1'
    gpio = 22
    player = tree_player(gpio_number=gpio, movie_1=movie1, movie_2=movie2)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
