import datetime
import json
from hmac import compare_digest
class Validator:
	def __init__(self,hmac):
		self.hmac=hmac.copy()

	def check(self,message):
		try:
			data=json.loads(message.decode('utf8'))
			payload=data['payload']
			hmac=data['hmac']
		except:
			return (None,'Invalid json format "{}"'.format(data))
		expected_hmac=calculate_hmac(payload)
		if not compare_digest(expected_hmac,hmac):
			return (None,'invalid HMAC "{}" for message "{}"'.format(hmac,payload))
		try:
			payload_data=json.loads(payload)
		except:
			return (None,'invalid payload "{}"'.format(payload))
		if not check_datetime(payload_data['datetime']):
			return (None,'invalid datetime "{}" for message "{}"'.format(datetime,payload))
		return (payload_data,None)

	def calculate_hmac(self,payload):
		hmac=self.hmac.copy()
		hmac.update(payload.encode('utf8'))
		return hmac.hexdigest()

def check_datetime(isotime):
	try:
		time=datetime.datetime.fromisoformat(isotime)
	except:
		return False # Time could not be converted to datetime object
	now=datetime.datetime.now(datetime.timezone.utc)
	delta=now-time
	return abs(delta.total_seconds())<60
