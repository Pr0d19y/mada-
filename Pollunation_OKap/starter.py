import RPi.GPIO as GPIO
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
elif not GPIO.input(zuccini_female_jmp):
    print "I'm female Zuccini!"
    from zuccini_female import *
elif not GPIO.input(tomato_jmp):
    print "I'm Tomato!"
    from tomato import *
elif not GPIO.input(zuccini_fruit_jmp):
    print "I'm Zuccini fruit!"
    from zuccini_fruit import *

#def runFSM(state):
#    while True:
#        print 'Starting state: {0}'.format(state.__name__)
#        state = state()

if __name__=='__main__':
    print 'main function of starter launched'
    state_idle()
    GPIO.cleanup()
