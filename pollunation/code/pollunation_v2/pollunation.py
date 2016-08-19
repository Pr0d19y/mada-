import FSM
import socket
from whoami import whoami
from pycom import Reset
# from RPi import *

# debug = input(debug_jmp)
debug = 3

exec'fsm = FSM.{0}FSM(debug)'.format(whoami())

#while True:
if True:
	try:
		fsm.runFSM()
	except Reset:
		raise
		pass
	except socket.error as e:
		print e
		raise
		print 'Connection error, Resetting'
