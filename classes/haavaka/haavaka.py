from RPi.GPIO import *
setmode(BOARD)

# Determine Gender
male_jmp    = 
bi_jmp      =

setup(male_jmp, IN, pull_up_down=PUD_DOWN)
setup(bi_jmp,   IN, pull_up_down=PUD_DOWN)

if input(male_jmp):
    import male
elif input(bi_jmp):
    import bisex
else:
    import female

def runFSM(state):
    while True:
        state = state()
        
