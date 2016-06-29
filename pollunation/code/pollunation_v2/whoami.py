def whoami():
	sel_dict = {1:'Male',2:'Female',3:'Zuccini'}
	msg = '\t 1. Male\n\t 2. Female\n\t 3. Zuccini\n'
	sel=raw_input(msg)
	return sel_dict[int(sel)]
