import threading
import time
from datetime import datetime

class Beeper:
	def __init__(self, beep):
		self.beep=beep

	def confirm(self):
		tune=[0b11000001]
		self.beep(bytearray(tune))

	def keypress(self):
		tune=[0b11010101]
		self.beep(bytearray(tune))

	def ack(self):
		tune=[0b11010101,0b11000001]
		self.beep(bytearray(tune))

	def nak(self):
		tune=[0b11000001,0b11011011]
		self.beep(bytearray(tune))
