import logging
import datetime
import os
import RPi.GPIO as GPIO
import time
from omxplayer import OMXPlayer
import subprocess

# Const
CATCH_TIME_TH = 3 # seconds

# Set Video Files
idle_video_file = 'videos/tomato/tomato_blink_1024X600.mp4'
dust_complete_video_file = 'videos/tomato/tomato_after_1024X600.mp4'

# Set GPIO names
bee_on        = 38
bee_buzz      = 37
stop_gpio     = 40

running = True

def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=os.path.join('logs', 'tomato_{}.log'
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
        dust_complete_movie_controller.stop()
        time.sleep(0.5)
        #dust_complete_movie_controller.quit()
    except Exception as ex:
        logger.info('while trying to quit dust_complete player, got exception: {}'.format(ex))
    logger.info('quit_program finished')
    global running
    running = False
    time.sleep(0.5)
    subprocess.call('sudo pkill omxplayer', shell=True)


logger = logging.getLogger('tomato')

## Tomato (bi-sex) ##



GPIO.setmode(GPIO.BOARD)
GPIO.setup(bee_on      , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(bee_buzz    , GPIO.OUT)
GPIO.setup(stop_gpio      , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(stop_gpio, GPIO.FALLING, callback=quit_program, bouncetime=100)

GPIO.output(bee_buzz, True)


logger.info('creating omxplayer objects')
idle_movie_controller = OMXPlayer(filename=idle_video_file, args=['--loop', '--no-osd'])
dust_complete_movie_controller = OMXPlayer(filename=dust_complete_video_file, args=['--no-osd'])
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
        if not GPIO.input(bee_on):
            start_time = time.time()
            time.sleep(0.05)

        if (time.time() - start_time) >= CATCH_TIME_TH:
            logger.debug('bee detected')
            logger.debug('pausing idle movie')
            idle_movie_controller.pause()
            time.sleep(0.25)
            logger.debug('returning idle movie to starting position')
            idle_movie_controller.set_position(0)
            time.sleep(0.25)
            return state_dust_complete()


def state_dust_complete():
    logger.info('starting state_dust_complete')
    global dust_complete_movie_controller
    logger.debug('starting sync play of dust_complete movie')
    dust_complete_movie_controller.play_sync()
    logger.debug('sync play of dust_complete movie ended')
    dust_complete_movie_controller.quit()
    logger.debug('opening new object for dust_complete_movie_controller')
    dust_complete_movie_controller = OMXPlayer(filename=dust_complete_video_file, args=['--no-osd'])
    time.sleep(0.25)
    logger.debug('starting async play of idle movie')
    idle_movie_controller.play()

