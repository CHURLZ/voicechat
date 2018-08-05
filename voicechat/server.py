import queue
import socket
import logging
import threading
import sys
from workers import *

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
log = logging.getLogger()


class Server(Runner):
	"""Server object mediates between clients."""

	def __init__(self, host, port):
		super().__init__()
		self.host = host
		self.port = port
		self.setup()

	def setup(self):
		self.workers = []
		self.dataq = queue.Queue() 
		self.broadcast_worker = BroadcastWorker(self.dataq)

	def run(self):
		super().run()
		log.info(f'Starting server on port {self.port}')

		# Instatiating one broadcast worker to send all the audio recied from readers
		self.broadcast_worker.run()

		while self.running:
			try:
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.bind((self.host, self.port))
					s.listen(2)
					conn, addr = s.accept()
					s.setblocking(0)

					self.broadcast_worker.add_client(conn)
					rw = self.create_worker(conn, addr)
					rw.run()
			except socket.error as msg:
				log.info(str(msg))
			except ConnectionResetError as e:
				log.info(str(msg))
			except:
				log.info('hu')

	def create_worker(self, conn, addr):
		worker = ReadWorker(conn, addr, self.dataq)
		self.workers.append(worker)
		return worker


if __name__ == '__main__':
	s = Server(host='', port=5004)
	s.run()