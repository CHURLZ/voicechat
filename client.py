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






# 		receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
# send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# print("Voice chat running")

# def receive_data():
#     while True:
#         try:
#             data = s.recv(1024)
#             receive_stream.write(data)
#         except:
#             pass


# def send_data():
#     while True:
#         try:
#             data = send_stream.read(CHUNK)
#             s.sendall(data)
#         except:
#             pass

# thread.start_new_thread(receive_data, ())
# thread.start_new_thread(send_data, ())
