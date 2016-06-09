from RPi.GPIO import *
setmode(BOARD)

# Const
CATCH_TIME_TH = 3 # seconds

# Determine Gender
male_jmp    = 40
bi_jmp      = 33

setup(male_jmp, IN, pull_up_down=PUD_DOWN)
setup(bi_jmp,   IN, pull_up_down=PUD_DOWN)

if input(male_jmp):
    from male import *
elif input(bi_jmp):
    from bisex import *
else:
    from female import *

def runFSM(state):
    while True:
        print 'Starting state: {0}'.format(state.__name__)
        state = state()
        
if __name__=='__main__':
    runFSM(state_idle)
