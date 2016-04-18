__author__ = 'nfreiman'



class movie_player():
    """
    basic movie player
    Adi Sh
    """
    def __init__(self, movies_file):
        pass

    def play(self):
        pass

    # etc.


###########################  Yoatzim

class yoetz():
    """
    Or L
    """
    def __init__(self, gpio):
        self.my_player = movie_player(a)

    def gpio_callback(self):
        self.my_player.play()

###########################  Barcode

class barcode():
    """
    Omer K
    """

    def __init__(self, gpio):
        self.my_player = movie_player(a)

    # read from standard input, and according to barcode satrt movie


###########################  Big Tree

# Netanel F
class tree_player():
    def __init__(self, gpio):
        self.my_player1 = movie_player(a)
        self.my_player2 = movie_player(a)

    def gpio_callback(self):
        self.my_player1.stop()
        self.my_player2.play()


class tree_controller():
    """
    input: 2 values (water, sun)
    output:
    1. control chain velocity and direction
    2. conrol many servo motors for leaves
    3. conrol GPIOs for 4 tree players

    """
    pass


###########################  Bee

class bombos_bee():
    def __init__(self, gpio):
        self.my_player = movie_player(a)

    def optic_identification(self):
        pass


class honey_bee():
    def __init__(self, gpio):
        self.my_player = movie_player(a)

    def optic_identification(self):
        """
        if male: start led
        if male + female: start movie

        """
