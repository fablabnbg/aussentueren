import datetime
import json
from hmac import compare_digest
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
		except:
			return (None,'Invalid payload "{}"'.format(payload))
		if not check_datetime(payload_data.get('datetime','')):
			return (None,'Invalid datetime "{}" for message "{}"'.format(datetime,payload))
		return (payload_data,None)

	def calculate_hmac(self,payload):
		hmac=self.hmac.copy()
		hmac.update(payload.encode('utf8'))
		return hmac.hexdigest()

GRACE_PERIOD=60

def check_datetime(isotime):
	try:
		time=datetime.datetime.fromisoformat(isotime)
	except:
		return False # Time could not be converted to datetime object
	now=datetime.datetime.now(datetime.timezone.utc)
	try:
		delta=now-time
	except TypeError:
		return False # time has no timezone
	return abs(delta.total_seconds())<GRACE_PERIOD
