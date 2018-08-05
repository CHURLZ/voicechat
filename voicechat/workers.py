import logging
import threading

class Runner(object):
	def __init__(self):
		self.running = False

	def stop(self):
		self.running = False

	def run(self):
		self.running = True


class ReadWorker(Runner):

	CHUNK_SIZE = 512

	def __init__(self, client, addr, message_queue):
		super().__init__()
		self.message_queue = message_queue
		self.thread = threading.Thread(target=self.work, args=(client, addr))

	def run(self):
		super().run()
		self.thread.start()

	def work(self, client, address):
		with client:
			while self.running:
				data = client.recv(ReadWorker.CHUNK_SIZE)
				self.message_queue.put((data, client))


class BroadcastWorker(Runner):
					
	def __init__(self, message_queue):
		super().__init__()
		print(f'BroadcastWorker created!')
		self.message_queue = message_queue
		self.clients = []
		self.thread = threading.Thread(target=self.work)

	def add_client(self, client):
		self.clients.append(client)

	def run(self):
		super().run()
		self.thread.start()

	def work(self):
		while self.running:
			if self.clients and self.message_queue.qsize() > 0:
				(data, client) = self.message_queue.get()
				[c.send(data) for c in self.clients if c and c is not client]
