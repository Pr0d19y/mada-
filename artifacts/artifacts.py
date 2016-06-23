

__author__ = 'okapach'

from classes import omxplayer
import RPi.GPIO as GPIO
import artifacts_config as config


class artifact(object):
    """
    play a movie in a loop turn on a led when a button is pressed
    """

    def __init__(self, gpio_number, movie):
        print 'starting player'
        print 'movie: {}'.format(movie)
        print 'GPIO: {}'.format(gpio_number)

        self.control_gpio = gpio_number
        self.led_gpio = 38
        self.quit_gpio = 40
        self.movie = movie

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_gpio, GPIO.OUT)
        GPIO.output(self.led_gpio, 0)
        GPIO.add_event_detect(self.control_gpio, GPIO.FALLING, callback=self.event, bouncetime=50)
        GPIO.add_event_detect(self.quit_gpio, GPIO.FALLING, callback=self.quit, bouncetime=50)


        self.movie_controller = omxplayer.OMXPlayer(mediafile=self.movie, start_playback=True, args= '--loop --no-osd')


    def event(self, channel):
        GPIO.output(self.led_gpio, 1)
        time.sleep(config.LED_TIME)
        GPIO.output(self.led_gpio, 0)

    def quit(self, channel):
        GPIO.cleanup()
        self.movie_controller.stop()


if __name__ == '__main__':
    movie = config.movie
    gpio = 32
    player = artifact(gpio_number=gpio,  movie=movie)
