from logging import warn
from datetime import datetime

class Beeper:
	def __init__(self, beep):
		self.beep=beep
		self.tunes={
				'pin':[0b11010101,0b11000001],
				'deny':[0b11010101,0b11000001],
				'attention':[0b11010101,0b11000001],
				'keypress':[0b11010101,0b11000001],
				'confirm':[0b11010101,0b11000001],
				}

	def beep_by_style(self,style):
		print("beep ",style)
		tune=self.tunes.get(style,None)
		if tune is None:
			warn('Invalid style: "{}"'.format(style))
			return
		self.beep(bytearray(self.tunes[style]))

	def confirm(self):
		self.beep_by_style('confirm')

	def keypress(self):
		self.beep_by_style('keypress')
