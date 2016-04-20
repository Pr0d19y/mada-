__author__ = 'netanel'

#import movie_player
#import RPi.GPIO as GPIO


class tree_player(object):
    """
    control one screen on the "Big Tree display"
    toggle between two different movies according to GPIO input signal
    """

    def __init__(self, gpio_number, movie_1, movie_2):
        self.controll_gpio = gpio_number
        self.movie_1 = movie_1
        self.movie_2 = movie_2
        #self.movie_1_controller = movie_player.movie_player(movies_file=self.movie_1)
        #self.movie_2_controller = movie_player.movie_player(movies_file=self.movie_2)
        self.playing = True

    def play(self):
        while self.playing:
            state = self.read_state()
            '''
            play movie according to GPIO
            if state == first_movie_state:
                self.movie_2_controller.stop()
                self.movie_1_controller.play()

            '''
            # TODO: do we need to ensure the movie is played in a loop or maybe movie_player should have a loop() player

    def read_state(self):
        pass


if __name__ == '__main__':
    movie1 = r'path/to/movie1'
    movie2 = r'path/to/movie1'
    gpio = 2
    player = tree_player(gpio_number=gpio, movie_1=movie1, movie_2=movie2)
    player.play()
