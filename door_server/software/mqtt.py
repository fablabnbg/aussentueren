from logging import warn
import json
import datetime
import paho.mqtt.client as mqtt_client

def log(*args):
	print(args)

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
		payload_data,error=self.validator.check(message)
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
