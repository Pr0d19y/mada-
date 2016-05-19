__author__ = 'Or Levi'

#import movie_player
import barcode_config as config


class Barcode(object):
    """
    controls the barcode screen.
    activates a video according to barcode input.
    """

    def __init__(self, movie_1, movie_2, movie_3, movie_4):
        print 'starting player'
        print 'movie_1: {}'.format(movie_1)
        print 'movie_2: {}'.format(movie_2)
        print 'movie_3: {}'.format(movie_3)
        print 'movie_4: {}'.format(movie_4)

        self.movie_1 = movie_1
        self.movie_2 = movie_2
        self.movie_3 = movie_3
        self.movie_4 = movie_4

    def select_movie(self):
        barcode = str(input('READ BARCODE: '))
        if   barcode == config.BARCODE_1:
            print 'movie 1'
        elif barcode == config.BARCODE_2:
            print 'movie 2'
        elif barcode == config.BARCODE_3:
            print 'movie 3'          
        elif barcode == config.BARCODE_4:
            print 'movie 4'
        else:
            print 'no such barcode-' + barcode

if __name__ == '__main__':
    movie_1 = r'path/to/movie_1'
    movie_2 = r'path/to/movie_2'
    movie_3 = r'path/to/movie_3'
    movie_4 = r'path/to/movie_4'

    player = Barcode(movie_1=movie_1,movie_2=movie_2,movie_3=movie_3,movie_4=movie_4)

    while True:
        player.select_movie()
    
