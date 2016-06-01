__author__ = 'okapach'

from classes import omxplayer
import RPi.GPIO as GPIO


class artifact(object):
    """
    play a movie once and turn on a led when a button is pressed
    """

    def __init__(self, gpio_number, movie):
        print 'starting player'
        print 'movie: {}'.format(movie)
        print 'GPIO: {}'.format(gpio_number)

        self.control_gpio = gpio_number
        self.movie = movie

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.control_gpio, GPIO.FALLING, callback=self.event, bouncetime=50)

        self.movie_controller = omxplayer.OMXPlayer(mediafile=self.movie, start_playback=True)


    def event(self, channel):
        current_state = GPIO.input(self.control_gpio)
        self.movie_controller.stop()
        self.movie_controller = omxplayer.OMXPlayer(mediafile=self.movie, start_playback=True)
        print 'event detected, ch: {}, FALLING event'.format(channel)
        #self.movie_controller.toggle_pause()
        #self.movie_2_controller.toggle_pause()

    def quit(self):
        GPIO.cleanup()
        self.movie_controller.stop()


if __name__ == '__main__':
    movie = r'/home/pi/Downloads/tzaleket.mp4'
    gpio = 32
    player = artifact(gpio_number=gpio,  movie=movie)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()

