import datetime
import json
from logging import info, warn
from hmac import compare_digest

GRACE_PERIOD=60

class Validator:
	def __init__(self,hmac):
		self.hmac=hmac.copy()

	def check(self,message):
		try:
			data=json.loads(message.payload.decode('utf8'))
			payload=data['payload']
			hmac=data['hmac']
		except:
			return (None,'Invalid json format "{}"'.format(message))
		expected_hmac=self.calculate_hmac(payload)
		if not compare_digest(expected_hmac,hmac):
			return (None,'Invalid HMAC "{}" for message "{}". Expected "{}"'.format(hmac,payload,expected_hmac))
		try:
			payload_data=json.loads(payload)
			payload_datetime=payload_data.get('datetime', '')
		except:
			return (None,'Invalid payload "{}"'.format(payload))
		if not check_datetime(payload_datetime):
			return (None,'Invalid datetime "{}" for message "{}"'.format(payload_datetime,payload))
		return (payload_data,None)

	def calculate_hmac(self,payload):
		hmac=self.hmac.copy()
		hmac.update(payload.encode('utf8'))
		return hmac.hexdigest()


def check_datetime(isotime):
	try:
		time=datetime.datetime.fromisoformat(isotime)
	except:
		warn("check_datetime time could not be converted to datetime object")
		return False # Time could not be converted to datetime object
	now=datetime.datetime.now(datetime.timezone.utc)
	try:
		delta=now-time
	except TypeError:
		warn("check_datetime time has no timezone")
		return False # time has no timezone

	if abs(delta.total_seconds()) > GRACE_PERIOD:
		warn("check_datetime delta {:.2f} > GRACE_PERIOD {} (now: {} / time: {})".format(delta.total_seconds(), GRACE_PERIOD, now, time))
		return False
	else:
		info("check_datetime delta {:.2f} <= GRACE_PERIOD {} (now: {} / time: {})".format(delta.total_seconds(), GRACE_PERIOD, now, time))
		return True
