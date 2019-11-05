import threading
import time
from logging import info

class Lock_ctrl:
	"""The Lock_ctrl class manages the door lock.

	Opens the latch and activates the automatic closer.

	Lock_ctrl(IO_open,IO_close,IO_latch)
	IO_latch : IOctrl.gpio class controlling the doors latch
	IO_closer : IOctrl.gpio class controlling the door closer
	"""
	def __init__(self,IO_latch,IO_closer):
		self.latcher=IO_latch
		self.latcher.set_dir('out')
		self.latcher.set(0)
		self.closer=IO_closer
		self.closer.set_dir('out')
		self.closer.set(1)

	def latch(self):
		"""open the latch."""
		info('latch')
		self.latcher.tap(3)
		self.closer.set(0)

	def close(self):
		"""activate closer."""
		info('close')
		self.closer.set(1)
