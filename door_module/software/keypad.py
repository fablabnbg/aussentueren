import threading

class Keypad(threading.Thread):
	def __init__(self,dev,on_key,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.s=dev
		self.on_key=on_key
		self.lock=threading.RLock()
		self.flush()

	def run(self):
		while True:
			c=self.s.read(1).decode('ascii')
			if len(self.buffer)>100:
				self.flush()
			with self.lock:
				self.buffer+=c
			self.on_key(self.buffer)

	def flush(self):
		with self.lock:
			self.buffer=""

