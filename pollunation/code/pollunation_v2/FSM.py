import sys
sys.path.append(r'C:\Users\ocohen10\Documents\MadaMuzeum\pollunation_v2')

from pycom import Reset, pycom
import time

bee_on = None
video_list = []
class FSM:
	"""
	Inheriting Classes must implement functions for each state:
		State_1(self)
		State_2(self)
		...
	"""
	def __init__(self,debug):
		self.debug = debug
		self.comm = pycom(self.whoami, debug=debug)
		
	def runFSM(self):
		self.current_state = 0
		next_state = 1
		while True:
			self.current_state = next_state
			if self.debug: print "Running State: {}".format(self.current_state)
			next_state = self.runState(self.current_state)
			time.sleep(0.5)
			
	def runState(self, state):
		try:
			exec "state_func = self.State_{0}".format(state)
		except NameError:
			# raise NotImplementedError("State_{0} not implemented".format(state))
			if self.debug: print 'Attempt to run unimplemented state {0}\nReseting'.format(state)
			self.comm.send_err()
			raise Reset()
			
		try:
			ret = state_func()
			next_state = self.comm.run(ret)
			return next_state
		except Reset:
			print "Received Reset Command"
			for video in video_list:
				video.stop()
			raise
	
class MaleFSM(FSM):
	def __init__(self,debug):
		self.whoami = 'Male'
		FSM.__init__(self,debug)
		self.BEE_ANTI_BOUNCE = 3
		
		# idle_video_file = 

	def State_1(self):
		"""
		Idle
		Male Blink
		"""
		# blink_video.play()
		if self.debug: print 'blink_video.play()'
		# Wait for bee with anti-bounce
		start_time = time.time()
		while time.time() - start_time < self.BEE_ANTI_BOUNCE:
			if not self.input(bee_on):
				if self.debug>2: print '\tBee Off'
				start_time = time.time()
			time.sleep(0.1)
		if self.debug: print 'State 1 ended'
		return 2
	def State_2(self):
		"""
		Female Blink
		"""
		# blink_video.pause()
		if self.debug: print 'blink_video.pause()'
		# collect_video.play()
		if self.debug: print 'collect_video.play()'

		# Wait for bee with anti-bounce
		start_time = time.time()
		while time.time() - start_time < self.BEE_ANTI_BOUNCE:
			if not self.input(bee_on):
				if self.debug>2: print '\tBee Off'
				start_time = time.time()
			time.sleep(0.1)
		if self.debug: print 'State 2 ended'
		return 3
	def State_3(self):
		"""
		Pollunation Complete
		"""
		# collect_video.pause()
		if self.debug: print 'collect_video.pause()'
		time.sleep(1.5)
		# collect_video.restart()
		if self.debug: print 'collect_video.restart()'
		if self.debug: print 'State 3 ended'
		return 1

	# def input(self,null):
		# import random
		# return random.random() > 0.2
class FemaleFSM(FSM):
	def __init__(self,debug):
		self.whoami = 'Female'
		FSM.__init__(self,debug)
		# idle_video_file = 
	def State_1(self):
		"""
		Idle
		Male Blink
		"""
		# if not idle_video.isalive():
			# idle_video.play()
		if self.debug: print 'idle_video.play()'
		time.sleep(0.1)
		# idle_video.pause()
		if self.debug: print 'idle_video.pause()'
		if self.debug: print 'State 1 ended'
	def State_2(self):
		"""
		Female Blink
		"""
		# idle_video.play()
		if self.debug: print 'idle_video.play()'
		if self.debug: print 'State 2 ended'
	def State_3(self):
		"""
		Pollunation Complete
		"""
		# idle_video.pause()
		if self.debug: print 'idle_video.pause()'
		if self.debug: print 'State 3 ended'
		
class ZucciniFSM(FSM):
	def __init__(self,debug):
		self.whoami = 'Zuccini'
		FSM.__init__(self,debug)
		# idle_video_file = 
	def State_1(self):
		"""
		Idle
		Male Blink
		"""
		# if not idle_video.isalive():
			# idle_video.play()
		if self.debug: print 'idle_video.play()'
		time.sleep(0.1)
		# idle_video.pause()
		if self.debug: print 'idle_video.pause()'
		if self.debug: print 'State 1 ended'
	def State_2(self):
		"""
		Female Blink
		"""
		if self.debug: print 'State 2 ended'
	def State_3(self):
		"""
		Pollunation Complete
		"""
		# state_complete_video.play()
		if self.debug: print 'state_complete_video.play()'
		
		if self.debug: print 'State 3 ended'
