__author__ = 'Or Levi'

#import movie_player
import advisor_config as config
import time
import threading
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
        self.last_event_time = 0

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.control_gpio, GPIO.BOTH, callback=self.event, bouncetime=50)

    def event(self, channel):
        self.last_event_time = time.time()
        current_state = GPIO.input(self.control_gpio)
        if current_state:            
            print 'debug print : PLAY THREAD started'
            play_thread = threading.Thread(target=self.play_after_delay)
            play_thread.start() 
        else:  
            print 'debug print : STOP THREAD started'
            stop_thread = threading.Thread(target=self.pause_wait_and_stop)
            stop_thread.start()             

    def stop_prev_event_threads(self):
        ''' this method kills previous event threads (i.e threads that didnt finish delay phases) '''
        print "debug print : KILLING prev threads"

    def play_after_delay(self):
        ''' this method waits the DELAY_TIME specified in the config file, and then play the video ''' 
        time.sleep(config.DELAY_TIME)
        time_since_last_event = time.time() - self.last_event_time
        # make sure there wasn't another event since this method was called before executing any other commands
        if time_since_last_event >= config.DELAY_TIME:
            print "debug print : movie PLAY called"
            #self.movie_controller.play()
              
    def pause_wait_and_stop(self):
        ''' this method pauses the video, waits the PAUSE_TIME specified in the config file, and then
            stops the video '''
        print "debug print : movie PAUSE called"
        #self.movie_controller.pause()
        time.sleep(config.PAUSE_TIME)
        time_since_last_event = time.time() - self.last_event_time
        # make sure there wasn't another event since this method was called before executing any other commands
        if time_since_last_event >= config.PAUSE_TIME:
            print "debug print : movie STOP called"
            #self.movie_controller.stop()

    def quit(self):
        GPIO.cleanup()
        # TODO: threading cleanup needed?

if __name__ == '__main__':
    movie = r'path/to/movie'
    gpio = 22
    player = advisor(gpio_number=gpio, movie=movie)

    q = raw_input("Do you want to exit? (Y)")
    if q is 'Y':
        player.quit()
