import time

def main():
    from classes.omxplayer import OMXPlayer

    filename1 = '/home/pi/Haavaka/blink_test_02.mp4'
    filename2 = '/home/pi/Haavaka/all_avkanim.mp4'
    flags = '' #'--loop'

    pl1 = OMXPlayer(filename1, flags)
    pl1.pause()
    pl2 = OMXPlayer(filename2, flags)

    pl2.play()
    pl1.play()
    time.sleep(1)
    pl1.pause()
    time.sleep(0.2)
    pl2.play()
    time.sleep(1)
    pl2.pause()

    return pl1, pl2
