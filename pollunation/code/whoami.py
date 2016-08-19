import sys
from RPi.GPIO import *
setmode(BOARD)

# Determine Gender
male_jmp    = 40
bi_jmp      = 33
zuccini_jmp = 10

setup(male_jmp   ,   IN, pull_up_down=PUD_UP)
setup(bi_jmp     ,   IN, pull_up_down=PUD_UP)
setup(zuccini_jmp,   IN, pull_up_down=PUD_UP)

if not input(male_jmp):
    print 'I am Male'
elif not input(zuccini_jmp):
    print 'I am Zuccini'
elif not input(bi_jmp):
    print 'I am Tomato'
else:
    print 'I am Female'
