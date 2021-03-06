import re

PIN_LENGTH=4

def is_pin(buf):
	if not (len(buf)==PIN_LENGTH or len(buf)==PIN_LENGTH+1):
		return False
	if re.match('#?\d{{{}}}'.format(PIN_LENGTH),buf):
		return True
	return False

def is_pin_change(buf):
	pattern='\*(?P<oldpin>\d{{{length}}})#(?P<newpin>\d{{{length}}})#(?P=newpin)'.format(length=PIN_LENGTH)
	result=re.match(pattern,buf)
	if not result:
		return None
	return result.groupdict()
