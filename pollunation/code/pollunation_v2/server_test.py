import socket

SND = 's' #int('1010 1010'.replace(' ',''), 2)
AKN = 'k' #int('1100 1100'.replace(' ',''), 2)
ERR = 'er' #int('1110 0011'.replace(' ',''), 2)

class Server:
	def __init__(self):
		self.host = socket.gethostname()
		self.port = 10000
	def server_listen(self):
		server_address = (self.host, self.port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(server_address)
		# Listen for incoming connections
		self.sock.listen(1)
		while True:
			# Wait for a connection
			connection, client_address = self.sock.accept()
			try:
				# if client_address == male_address:
					message = connection.recv(2)
					print 'Recieved:\n{0}'.format(message)
					# import pdb
					# pdb.set_trace()
					if message[0] == SND:
						next_state = ord(message[1])
						ret_message = AKN + chr(next_state)
						print 'Sending:\n{0}'.format(ret_message)
						connection.sendall(ret_message)
						return next_state
					else:
						ret_message = ERR
						print 'Sending:\n{0}'.format(ret_message)
						connection.sendall(ret_message)
						if self.debug: print >>sys.stderr, 'Recieved Error from client, restarting'
						raise Reset()
			finally:
				# Clean up the connection
				connection.close()
				self.sock.close()
				print 'Connection closed'
class Client:
	def __init__(self):
		self.host = socket.gethostname()
		self.port = 10001
		self.server_port = 10000
	### CLIENT
	def Male(self, next_state):
		female_ret = self.send_state(female_address, next_state)
		zucc_ret   = self.send_state(zucc_address, next_state)
		if not female_ret or not zucc_ret:
			self.send_err()
			raise Reset()
		return next_state
		
	def send_state(self, next_state):
		server_address = (self.host, self.server_port)
		# Connect the socket to the port where the server is listening
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(server_address)
		try:
			# Send data
			message = SND + chr(next_state)
			print 'Sending:\n{0}'.format(message)
			self.sock.sendall(message)

			# Look for the response
			msg_expected = AKN + chr(next_state)
			
			data = self.sock.recv(2)
			print 'Recieved:\n{0}'.format(data)
			return data == msg_expected
		finally:
			self.sock.close()
			print 'Connection closed'
			
	def send_err(self):
		for server_address in [female_address, zucc_address]:
			# Connect the socket to the port where the server is listening
			self.sock.connect(server_address)
			try:
				# Send error
				message = ERR
				self.sock.sendall(message)
				# No response needed
			finally:
				self.sock.close()
class Reset(Exception):
	def __init__(self):
		pass