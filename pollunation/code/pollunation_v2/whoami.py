def whoami(manual = False, debug = 0):
	if manual:
		sel_dict = {1:'Male',2:'Female',3:'Zuccini'}
		msg = '\t 1. Male\n\t 2. Female\n\t 3. Zuccini\n'
		sel=raw_input(msg)
		return sel_dict[int(sel)]
	else:
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
		    if debug: print 'I am Male'
		    return 'Male'
		elif not input(zuccini_jmp):
		    if debug: print 'I am Zuccini'
		    return 'Zuccini'
		elif not input(bi_jmp):
		    if debug: print 'I am Tomato'
		    return 'Tomato'
		else:
		    if debug: print 'I am Female'
		    return 'Female'
