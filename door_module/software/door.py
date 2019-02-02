import threading

class Door:
	"""The Door class can check the status of the door.

	Door(IO_door)
	IO_door : IOctrl.gpio class controlling the pin the door sensor is connected to
	"""
	def __init__(self,IO_door,open_callback=None,close_callback=None):
		self.gpio=IO_door
		self.gpio.set_dir('in')
		self.open_callback=open_callback
		self.close_callback=close_callback
		if self.open_callback or self.close_callback:
			self.abort=False
			self.gpio.set_interrupt('both')
			threading.Thread(target=self.wait_change).start()
	
	def is_open(self):
		"Returns True if door is open"
		return self.gpio.get()==1

	def is_closed(self):
		"Returns True if door is closed"
		return self.gpio.get()==0

	def wait_change(self):
		"Wait for change in door status and call callback"
		while not self.abort:
			self.gpio.wait()
			if self.is_open():
				if self.open_callback:
					self.open_callback()
			else:
				if self.close_callback:
					self.close_callback()
