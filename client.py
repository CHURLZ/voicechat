# Echo client program
import socket
import time
import sys


HOST = 'localhost'
PORT = int(sys.argv[1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print('starting client...')
	while True:
		s.sendall(b'Hello, world')
		data = s.recv(1024)
		print('Received', repr(data))