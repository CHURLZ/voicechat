import socket
import time
import sys
import pyaudio
import threading
import numpy as np

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])

print(f'Connecting to: {HOST}, {PORT}')

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MIN_VOLUME = int(sys.argv[3])
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
	prev_vol = 0
	while True:
		try:
			string_audio = send_stream.read(CHUNK)
			data_chunk = np.fromstring(string_audio, dtype=np.int16)
			vol = max(data_chunk)
			smoother_vol = (vol+prev_vol)/2

			if(smoother_vol >= MIN_VOLUME):
				print(f'size: {len(bytes(data_chunk))}')
				s.sendall(data_chunk)
			prev_vol = vol
		except Exception as e:
			print(e)

threading.Thread(target=receive_data).start()
threading.Thread(target=send_data).start()

while True:
	pass