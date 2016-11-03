__author__ = 'Or Levi'

import sys
import advisor_config as config
import time
import threading
import RPi.GPIO as GPIO
#sys.path.append('/home/pi/mada-/classes/')
import classes.ip_reservations as ip_reservations
from classes.omxplayer import OMXPlayer

class advisor(object):
    """
    controls one advisor screen.
    activates the advisor video according to GPIO input.
    """

    def __init__(self, gpio_number, movie):
        #print 'starting player'
        #print 'movie: {}'.format(movie)
        #print 'GPIO: {}'.format(gpio_number)

        self.control_gpio = gpio_number
        self.stop_gpio = 40
        self.movie = movie
        self.current_state = None
        self.polling_tries = 0
        self.last_event_time = 0
        self.last_event_was_play = True

        self.movie_controller = OMXPlayer(mediafile=self.movie,args="--loop -o local")
        if self.movie == r'/home/pi/Downloads/dan_levanon.mp4':
            ip_reservations.set_static_ip(ip_reservations.IPS['dan_levanon'])
        elif self.movie == r'/home/pi/Downloads/market_intreviews.mp4':
            ip_reservations.set_static_ip(ip_reservations.IPS['market_intreviews'])
        elif self.movie == r'/home/pi/Downloads/uri_ariel.mp4':
            ip_reservations.set_static_ip(ip_reservations.IPS['uri_ariel'])
        elif self.movie == r'/home/pi/Downloads/eyal_kimchi.mp4':
            ip_reservations.set_static_ip(ip_reservations.IPS['eyal_kimchi'])

        GPIO.setmode(GPIO.BOARD)  # use board numbers (ie pin1, pin2 of board and not of the chip)
        GPIO.setup(self.control_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.stop_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.stop_gpio, GPIO.FALLING, callback=self.quit, bouncetime=100)
        self.running = True

        self.movie_controller.play()#######################################################################
        time.sleep(config.STARTUP_PLAY_TIME)
        
        self.pin_poll_thread = threading.Thread(target=self.poll_input)
        self.pin_poll_thread.start()
        

    def event(self):
        self.last_event_time = time.time()
        if self.current_state:
            #print "debug print : play_thread"
            self.last_event_was_play = False
            stop_thread = threading.Thread(target=self.pause_wait_and_stop)
            stop_thread.start() 
        else:  
            #print "debug print : stop_thread"
            self.last_event_was_play = True
            play_thread = threading.Thread(target=self.play_after_delay)
            play_thread.start()             

    def poll_input(self):
        while self.running:
            current_state = GPIO.input(self.control_gpio)
            if current_state != self.current_state and self.polling_tries == config.POLLING_TRIES:  #state has changed and reached stable value
                self.current_state = current_state
                self.event()
            elif current_state != self.current_state and self.polling_tries < config.POLLING_TRIES: #state has changed but we are still waiting for input to stabilize
                self.polling_tries = self.polling_tries + 1
            else:                                                                                   #stete has not changed, reset the stability count
                self.polling_tries = 1                
            time.sleep(config.POLLING_DELAY)
        #print "debug print : quitting poll_input function"
            
    def play_after_delay(self):
        ''' this method waits the DELAY_TIME specified in the config file, and then play the video ''' 
        time.sleep(config.DELAY_TIME)
        time_since_last_event = time.time() - self.last_event_time
        # make sure there wasn't another event since this method was called before executing any other commands
        if time_since_last_event >= config.DELAY_TIME and self.last_event_was_play:
            #print "debug print : movie PLAY called"
            self.movie_controller.play()
              
    def pause_wait_and_stop(self):
        ''' this method pauses the video, waits the PAUSE_TIME specified in the config file, and then
            stops the video '''
        #print "debug print : movie PAUSE called"
        self.movie_controller.pause()
        time.sleep(config.PAUSE_TIME)
        time_since_last_event = time.time() - self.last_event_time
        # make sure there wasn't another event since this method was called before executing any other commands
        if time_since_last_event >= config.PAUSE_TIME and not self.last_event_was_play:
            #print "debug print : movie STOP called"
            self.movie_controller.restart()
            #self.movie_controller.stop()
            #self.movie_controller = OMXPlayer(mediafile=self.movie,args="--win 0,0,400,400")
            

    def quit(self, channel):
        #print "debug print: Quitting"
        #GPIO.cleanup()
        self.movie_controller.stop()
        time.sleep(0.1)
        self.running = False

       # TODO: threading cleanup needed?

if __name__ == '__main__':
    movie = config.movie
    gpio = 32
    player = advisor(gpio_number=gpio, movie=movie)
