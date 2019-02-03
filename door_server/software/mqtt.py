from logging import warn
import json
import datetime
import paho.mqtt.client as mqtt_client
from hmac import compare_digest

def log(*args):
	print(args)

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
		expected_hmac=calculate_hmac(self.hmac.copy(),payload)
		if not compare_digest(expected_hmac,hmac):
			return (None,'invalid HMAC "{}" for message "{}"'.format(hmac,payload))
		try:
			payload_data=json.loads(payload)
		except:
			return (None,'invalid payload "{}"'.format(payload))
		if not check_datetime(payload_data['datetime']):
			return (None,'invalid datetime "{}" for message "{}"'.format(datetime,payload))
		return (payload_data,None)

class Mqtt:
	def __init__(self,addr,validator,interpreter):
		self.validator=validator
		self.interpreter=interpreter
		self.client=mqtt_client.Client()
		self.client.on_connect=self.on_connect
		self.client.on_message=self.on_message
		#self.client.on_log=log
		self.client.connect_async(addr)

	def start(self):
		self.client.loop_forever()

	def stop(self):
		self.client.loop_stop()
		
	def on_connect(self,client, userdata, flags, rc):
		print('Mqtt connected',rc)
		self.client.subscribe("doors/+/open")
		self.client.subscribe("doors/+/card_shown_outside")
		self.client.subscribe("doors/+/card_shown_inside")

	def on_message(self,client, userdata, message):
		_,door_name,request=message.topic.split('/')
		payload_data,error=validator.check(message)
		if not error is None:
			warn(error)
			return
		self.interpreter.do(door_name,request,payload_data['data'])

	def send(self,doorname,data):
		topic="doors/{}/command".format(doorname)
		payload=dict()
		payload['datetime']=datetime.datetime.now(datetime.timezone.utc).isoformat()
		payload['command']=data
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
	now=datetime.datetime.now(datetime.timezone.utc)
	delta=now-time
	return abs(delta.total_seconds())<60
