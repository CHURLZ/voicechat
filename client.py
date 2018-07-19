# Echo client program
import socket
import time
import sys
import pyaudio
import threading

HOST = 'localhost'
PORT = int(sys.argv[1])

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

p = pyaudio.PyAudio()


receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Voice chat running")

def receive_data():
    while True:
        try:
            data = s.recv(1024)
            receive_stream.write(data)
        except:
            pass


def send_data():
    while True:
        try:
            data = send_stream.read(CHUNK)
            s.sendall(data)
        except:
            pass

threading.Thread(target=receive_data).start()
threading.Thread(target=send_data).start()

while True:
	pass


	# print('starting client...')
	# while True:
	# 	s.sendall(b'Hello, world')
	# 	data = s.recv(1024)
	# 	print('Received', repr(data))







