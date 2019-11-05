import threading
import time
from logging import info

class Lock_ctrl:
	"""The Lock_ctrl class manages the door lock.

	Currently only opens the latch

	Lock_ctrl(IO_open,IO_close,IO_latch)
	IO_latch : IOctrl.gpio class controlling the doors latch
	"""
	def __init__(self,IO_latch):
		self.latcher=IO_latch
		self.latcher.set_dir('out')
		self.latcher.set(0)

	def latch(self):
		"""open the latch."""
		info('latch')
		self.latcher.tap(3)
