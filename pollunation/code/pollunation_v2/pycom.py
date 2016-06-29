import socket, sys, time

class Reset(Exception):
	def __init__(self, message='Reset detected'):
		self.message = message
		
class pycom:
	def __init__(self, whoami, debug=0):
	
		self.debug = debug

		self.SND = 's' 
		self.AKN = 'k' 
		self.ERR = 'er'
		
		self.male_address   = '127.0.0.1'
		self.female_address = '127.0.0.1'
		self.zucc_address   = '127.0.0.1'
		self.male_port      = 10000
		self.female_port    = 10001
		self.zucc_port      = 10002
		
		self.male_full_address   = (self.male_address, self.male_port) # Client
		self.female_full_address = (self.female_address, self.female_port) # Server #1
		self.zuccini_full_address   = (self.zucc_address, self.zucc_port) # Server #2
		
		exec "self.full_address = self.{0}_full_address".format(whoami.lower())
		self.host = socket.gethostname()

		exec "self.run = self.run{0}".format(whoami)

	def runFemale(self, ret = None):
		if self.debug: print >>sys.stderr, 'starting up female server on %s port %s' % self.female_full_address
		return self.server_listen(self.female_full_address)
	def runZuccini(self, ret = None):
		if self.debug: print >>sys.stderr, 'starting up Zuccini server on %s port %s' % self.zuccini_full_address
		return self.server_listen(self.zuccini_full_address)

	def server_listen(self, server_address):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(server_address)
		# Listen for incoming connections
		self.sock.listen(1)
		import pdb
		# pdb.set_trace()

		if 1: # while True:
			# Wait for a connection
			connection, client_full_address = self.sock.accept()
			client_address, client_port = client_full_address
			try:
				if client_address == self.male_address:
					message = connection.recv(2)
					print 'Recieved:\n{0}'.format(message)
					if message[0] == self.SND:
						next_state = ord(message[1])
						ret_message = self.AKN + chr(next_state)
						print 'Sending:\n{0}'.format(ret_message)
						connection.sendall(ret_message)
						return next_state
					else:
						ret_message = self.ERR
						print 'Sending:\n{0}'.format(ret_message)
						# connection.sendall(ret_message)
						self.send(connection, message)
						
						if self.debug: print >>sys.stderr, 'Recieved Error from client, restarting'
						raise Reset()
			finally:
				# Clean up the connection
				time.sleep(0.5)
				connection.close()
				if self.debug: print 'Connection Closed'
		self.sock.close()
		if self.debug: print 'Socket Closed'
		
	### CLIENT
	def runMale(self, next_state):
		female_ret = self.send_state(self.female_full_address, next_state)
		zucc_ret   = self.send_state(self.zuccini_full_address, next_state)
		if not female_ret or not zucc_ret:
			self.send_err()
			raise Reset()
		return next_state
		
	def send(self, sock, msg):
		"""
		Simply send the message through the socket
		for debug, one can induce errors into the message here
		"""
		# from random import random
		# rnd = random()
		# if rnd>0.95:
			# print 'Induced Error'
			# msg = chr(ord(msg[0])+1) + msg[1]
		# if rnd<0.05:
			# print 'Induced Error'
			# msg = msg[0] + chr(ord(msg[1])+1)
		sock.sendall(msg)
		
	def send_state(self, server_address, next_state):
		# Connect the socket to the port where the server is listening
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(server_address)
		try:
			# Send data
			message = self.SND + chr(next_state)
			print 'Sending:\n{0}'.format(message)
			# self.sock.sendall(message)
			self.send(self.sock, message)
			
			# Look for the response
			msg_expected = self.AKN + chr(next_state)
			
			data = self.sock.recv(2)
			print 'Recieved:\n{0}'.format(data)
			return data == msg_expected
		finally:
			time.sleep(0.5)
			self.sock.close()
			
	def send_err(self):
		for server_address in [self.female_full_address, self.zuccini_full_address, self.male_full_address]:
			
			if server_address == self.full_address:
				continue
				
			# Connect the socket to the port where the server is listening
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect(server_address)
			try:
				# Send error
				message = self.ERR
				# self.sock.sendall(message)
				self.send(self.sock, message)
				# No response needed
			finally:
				time.sleep(0.5)
				self.sock.close()
