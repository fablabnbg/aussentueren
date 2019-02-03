from logging import warn
import json
import datetime
import paho.mqtt.client as mqtt_client

def log(*args):
	print(args)

class Mqtt:
	def __init__(self,addr,name,validator,interpreter):
		self.validator=validator
		self.name=name
		self.interpreter=interpreter
		self.client=mqtt_client.Client()
		self.client.on_connect=self.on_connect
		self.client.on_message=self.on_message
		#self.client.on_log=log
		self.client.connect_async(addr)
		self.client.loop_start()

	def stop(self):
		self.client.loop_stop()
		
	def on_connect(self,client, userdata, flags, rc):
		client.subscribe("doors/{}/command".format(self.name))

	def on_message(self,client, userdata, message):
		payload_data,error=self.validator.check(message)
		if not error is None:
			warn(error)
			return
		self.interpreter.do(payload_data['command'])

	def send(self,subtopic,data,retain=False):
		topic="doors/{}/{}".format(self.name,subtopic)
		payload=dict()
		payload['datetime']=datetime.datetime.now(datetime.timezone.utc).isoformat()
		payload['data']=data
		payload_json=json.dumps(payload)
		message=dict()
		message['payload']=payload_json
		message['hmac']=self.validator.calculate_hmac(message['payload'])
		self.client.publish(topic,json.dumps(message),retain=retain)
