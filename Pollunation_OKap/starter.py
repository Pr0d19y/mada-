import sys
import RPi.GPIO as GPIO
sys.path.append('/home/pi/mada-/classes/')
import ip_reservations
GPIO.setmode(GPIO.BOARD)

# Const
CATCH_TIME_TH = 3 # seconds

# Determine Type
zuccini_fruit_jmp = 29
zuccini_male_jmp    = 19
zuccini_female_jmp= 26
tomato_jmp      = 33


GPIO.setup(zuccini_fruit_jmp   ,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tomato_jmp     ,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(zuccini_male_jmp,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(zuccini_female_jmp,   GPIO.IN, pull_up_down=GPIO.PUD_UP)



if not GPIO.input(zuccini_male_jmp):
    print "I'm male Zuccini!"
    from zuccini_male import *
    ip_reservations.set_static_ip(ip_reservations.IPS['pollination_zuc_male'])
elif not GPIO.input(zuccini_female_jmp):
    print "I'm female Zuccini!"
    from zuccini_female import *
    ip_reservations.set_static_ip(ip_reservations.IPS['pollination_zuc_female'])
elif not GPIO.input(tomato_jmp):
    print "I'm Tomato!"
    from tomato import *
    ip_reservations.set_static_ip(ip_reservations.IPS['pollination_tomato'])
elif not GPIO.input(zuccini_fruit_jmp):
    print "I'm Zuccini fruit!"
    from zuccini_fruit import *
    ip_reservations.set_static_ip(ip_reservations.IPS['pollination_zuc_fruit'])

#def runFSM(state):
#    while True:
#        print 'Starting state: {0}'.format(state.__name__)
#        state = state()

if __name__=='__main__':
    print 'main function of starter launched'
    state_idle()
    GPIO.cleanup()
