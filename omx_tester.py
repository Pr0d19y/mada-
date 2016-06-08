import time

def main():
    from classes.omxplayer import OMXPlayer

    movie_1 = '/home/pi/Haavaka/blink_test_02.mp4'
    movie_2 = '/home/pi/Haavaka/all_avkanim.mp4'

    movie_1_controller = omxplayer.OMXPlayer(mediafile=movie_1, args='--loop')
    time.sleep(0.5)
    movie_1_controller.toggle_pause()
    movie_2_controller = omxplayer.OMXPlayer(mediafile=movie_2, args='--loop', start_playback=True)
    time.sleep(0.5)

    time.sleep(1)
    
    movie_2_controller.toggle_pause()
    movie_1_controller.toggle_pause()

    time.sleep(1)

    movie_2_controller.toggle_pause()
    movie_1_controller.toggle_pause()

    time.sleep(1)

    movie_2_controller.stop()
    movie_1_controller.stop()

main()
