import hmac
import logging

import config
from mqtt import Mqtt
from interpreter import Interpreter
from status import StatusManager

logging.basicConfig(level=logging.DEBUG)

def open_door(door_name):
	print('open',door_name)
	mqtt.send(door_name,{'type':'open'})

def alarm_door(door_name,reason):
	reason2style={
			'pin':('outside','pin'),
			'deny':('outside','deny'),
			'close':('inside','confirm'),
			'attention':('all','attention'),
			'pin_changed':('outside','confirm'),
			}
	style=reason2style[reason]
	mqtt.send(door_name,{'type':'beep','beepstyle':style[1],'location':style[0]})

hmac_calculator=hmac.new(config.hmac_key,digestmod='sha512')
status=StatusManager()
interpreter=Interpreter(status_manager=status,open_door=open_door,alarm_door=alarm_door)
mqtt=Mqtt(addr=config.mqtt_broker,hmac=hmac_calculator,interpreter=interpreter)
mqtt.start()

