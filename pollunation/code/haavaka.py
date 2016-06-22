import sys
from RPi.GPIO import *
setmode(BOARD)

# Determine Gender
male_jmp    = 40
tomato_jmp  = 33
zuccini_jmp = 10

setup(male_jmp   ,   IN, pull_up_down=PUD_UP)
setup(tomato_jmp ,   IN, pull_up_down=PUD_UP)
setup(zuccini_jmp,   IN, pull_up_down=PUD_UP)

if not input(male_jmp):
    print 'I am Male'
    from male import *
elif not input(zuccini_jmp):
    print 'I am Zuccini'
    from zuccini import *
elif not input(tomato_jmp):
    print 'I am Tomato'
    from tomato import *
else:
    print 'I am Female'
    from female import *

def runFSM(state):
    while True:
        print 'Starting state: {0}'.format(state.__name__)
        state = state()

if __name__=='__main__':
    runFSM(state_idle)
