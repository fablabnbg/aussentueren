from logging import warn
import json
import datetime
import paho.mqtt.client as mqtt_client
import hmac
class Mqtt:
	def __init__(self,addr,name,hmac,interpreter):
		self.hmac=hmac.copy()
		self.name=name
		self.interpreter=interpreter
		self.client=mqtt_client.Client()
		self.client.on_connect=self.on_connect
		self.client.on_message=self.on_message
		self.client.connect_async(addr)
		self.client.loop_start()

	def stop(self):
		self.client.loop_stop()
		
	def on_connect(self,client, userdata, flags, rc):
		client.subscribe("doors/{}/#".format(self.name))

	def on_message(self,client, userdata, message):
		try:
			data=json.loads(message.payload.decode('utf8'))
			payload=data['payload']
			hmac=data['hmac']
		except:
			return # Ignore messages that are not valid json or don't contain payload and hmac
		expected_hmac=calculate_hmac(self.hmac.copy(),payload)
		if not hmac.compare_digests(expected_hmac,hmac):
			logging.warn('invalid HMAC "{}" for message "{}".format(hmac,payload)')
			return
		try:
			payload_data=json.loads(payload)
		except:
			logging.warn('invalid payload "{}".format(payload)')
			return # Ignore non JSON payloads
		if not check_datetime(payload_data['datetime']):
			logging.warn('invalid datetime "{}" for message "{}".format(datetime,payload)')
			return
		self.interpreter.do(payload_data['command'])

	def send(self,subtopic,data):
		topic="doors/{}/{}".format(self.name,subtopic)
		payload=dict()
		payload['datetime']=datetime.datetime.now(datetime.timezone.utc).isoformat()
		payload['data']=data
		payload_json=json.dumps(payload)
		message=dict()
		message['payload']=payload_json
		message['hmac']=calculate_hmac(self.hmac.copy(),message['payload'])
		self.client.publish(topic,json.dumps(message))

def calculate_hmac(hmac,payload):
	hmac.update(payload.encode('utf8'))
	return hmac.hexdigest()

def check_datetime(isotime):
	try:
		time=datetime.datetime.fromisoformat(isotime)
	except:
		return False # Time could not be converted to datetime object
	now=datetime.datetime.now(datetime.timezone.utc).isoformat()
	delta=now-time
	return abs(delta.total_seconds())<60
