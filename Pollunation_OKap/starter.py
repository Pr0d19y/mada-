import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# Const
CATCH_TIME_TH = 3 # seconds

# Determine Type
zuccini_male_jmp    = 40
zuccini_female_jmp= 29
tomato_jmp      = 33


#GPIO.setup(male_jmp   ,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tomato_jmp     ,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(zuccini_male_jmp,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(zuccini_female_jmp,   GPIO.IN, pull_up_down=GPIO.PUD_UP)



if not GPIO.input(zuccini_male_jmp):
    print "I'm male Zuccini!"
    #from male import *
elif not GPIO.input(zuccini_female_jmp):
    print "I'm female Zuccini!"
    #from zuccini import *
elif not GPIO.input(tomato_jmp):
    print "I'm Tomato!"
    from tomato import *
else:
    print "I'm something else!"
    #from female import *

#def runFSM(state):
#    while True:
#        print 'Starting state: {0}'.format(state.__name__)
#        state = state()

if __name__=='__main__':
    print 'main function of starter launched'
    state_idle()
    GPIO.cleanup()
