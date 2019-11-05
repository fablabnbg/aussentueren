from logging import warn,info
from datetime import datetime
from parameters import tunes

class Beeper:
	def __init__(self, beep):
		self.beep=beep

	def beep_by_style(self,style):
		info("beep {}".format(style))
		tune=tunes.get(style,None)
		if tune is None:
			warn('Invalid style: "{}"'.format(style))
			return
		self.beep(bytearray(tune))

	def confirm(self):
		self.beep_by_style('confirm')

	def keypress(self):
		self.beep_by_style('keypress')
