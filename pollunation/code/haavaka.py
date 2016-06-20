import sys
from RPi.GPIO import *
setmode(BOARD)

global debug
if len(sys.argv)>0:
    debug = sys.argv[0]
else:
    debug = 1

# Const
CATCH_TIME_TH = 3 # seconds

# Determine Gender
male_jmp    = 40
bi_jmp      = 33
zuccini_jmp = 10

setup(male_jmp   ,   IN, pull_up_down=PUD_UP)
setup(bi_jmp     ,   IN, pull_up_down=PUD_UP)
setup(zuccini_jmp,   IN, pull_up_down=PUD_UP)

if not input(male_jmp):
    print 'I am Male'
    from male import *
elif not input(zuccini_jmp):
    print 'I am Zuccini'
    from zuccini import *
elif not input(bi_jmp):
    print 'I am Tomato'
    from bisex import *
else:
    print 'I am Female'
    from female import *

def runFSM(state):
    while True:
        print 'Starting state: {0}'.format(state.__name__)
        state = state()

if __name__=='__main__':
    runFSM(state_idle)
