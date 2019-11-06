from logging import warn
import json
import datetime
import paho.mqtt.client as mqtt_client

def log(*args):
	print(args)

class Mqtt:
	def __init__(self,addr,validator,interpreter,status_manager):
		self.validator=validator
		self.interpreter=interpreter
		self.status_manager=status_manager
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
		self.client.will_set("status/doorserver/lwt","offline",qos=1,retain=True)
		self.client.publish("status/doorserver/lwt","online",qos=1,retain=True)
		self.status_manager.publish()
		self.client.subscribe("doors/+/open")
		self.client.subscribe("doors/+/card_shown_outside")
		self.client.subscribe("doors/+/card_shown_inside")
		self.client.subscribe("status/doorserver/public/set")

	def on_message(self,client, userdata, message):
		if message.topic=="status/doorserver/public/set":
			return self.interpreter.do_public(message.payload)
		_,door_name,request=message.topic.split('/')
		payload_data,error=self.validator.check(message)
		if not error is None:
			warn(error)
			return
		self.interpreter.do(door_name,request,payload_data['data'])

	def send(self,doorname,data):
		topic="doors/{}/command".format(doorname)
		message=prepare_message(self.validator.calculate_hmac,data)
		self.client.publish(topic,message)

	def simple_send(self,topic,message,retain=False):
		self.client.publish(topic,message,retain=retain)

def prepare_message(hmac_calculator,data):
		payload=dict()
		payload['datetime']=datetime.datetime.now(datetime.timezone.utc).isoformat()
		payload['command']=data
		payload_json=json.dumps(payload)
		message=dict()
		message['payload']=payload_json
		message['hmac']=hmac_calculator(message['payload'])
		return json.dumps(message)
