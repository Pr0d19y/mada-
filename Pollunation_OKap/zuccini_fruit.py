import logging
import datetime
import os
import RPi.GPIO as GPIO
import time
from omxplayer import OMXPlayer
import subprocess

# Const
DEBOUNCE_TIME_TH = 0.2 # seconds

# Set Video Files
idle_video_file = 'videos/zuccini/zuccini_fruit_1920x1080/zuccini_fruit_idle_1920x1080.mp4'
after_video_file = 'videos/zuccini/zuccini_fruit_1920x1080/zuccini_fruit_after_1920x1080.mp4'

# Set GPIO names
female_to_fruit_i = 35
force_stop_gpio_i = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setup(female_to_fruit_i      , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(force_stop_gpio_i      , GPIO.IN, pull_up_down=GPIO.PUD_UP)

running = True

def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'fruit_zuccini_{}.log'
                                                          .format(datetime.datetime.now()
                                                                  .strftime('%d-%m-%y_%H-%M-%S'))))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)

init_logging()


def quit_program(event):

    logger.info('in quit_program')
    
    try:
        idle_movie_controller.stop()
        time.sleep(0.5)
        #idle_movie_controller.quit()
    except Exception as ex:
        logger.info('while trying to quit idle player, got exception: {}'.format(ex))

    try:
        after_movie_controller.stop()
        time.sleep(0.5)
        #after_movie_controller.quit()
    except Exception as ex:
        logger.info('while trying to quit after player, got exception: {}'.format(ex))

        
    logger.info('quit_program finished')
    global running
    running = False
    time.sleep(0.5)
    subprocess.call('sudo pkill omxplayer', shell=True)

GPIO.add_event_detect(force_stop_gpio_i, GPIO.FALLING, callback=quit_program, bouncetime=100)
logger = logging.getLogger('fruit_zuccini')



logger.info('creating omxplayer objects')
idle_movie_controller = OMXPlayer(filename=idle_video_file, args=['--loop', '--no-osd'])
after_movie_controller = OMXPlayer(filename=after_video_file, args=['--no-osd'])
logger.info('finished creating omxplayer objects')


def state_idle():
    logger.info('starting idle movie')
    idle_movie_controller.play()
    while running:
        state_bee_on()

def state_bee_on():
    logger.info('starting state_bee_on')
    start_time = time.time()
    while running:
        if not GPIO.input(female_to_fruit_i):
            start_time = time.time()
            time.sleep(0.05)

        if (time.time() - start_time) >= DEBOUNCE_TIME_TH:
            logger.debug('bee detected')
            logger.debug('pausing idle movie')
            idle_movie_controller.pause()
            time.sleep(0.1)
            logger.debug('returning idle movie to starting position')
            idle_movie_controller.set_position(0)
            time.sleep(0.1)
            return state_bee_pollunated()

def state_bee_pollunated():
    logger.info('starting state_after')
    global after_movie_controller
    logger.debug('starting sync play of after movie')
    after_movie_controller.play_sync()
    logger.debug('sync play of after movie ended')
    after_movie_controller.quit()
    logger.debug('opening new object for after_movie_controller')
    after_movie_controller = OMXPlayer(filename=after_video_file, args=['--no-osd'])
    time.sleep(0.25)
    idle_movie_controller.play()
