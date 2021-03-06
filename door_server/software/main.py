#!/usr/bin/env python3
import sys
version=sys.version_info
if version.major<3:
	raise RuntimeError("Need python 3")
if version.minor<7:
	from backports.datetime_fromisoformat import MonkeyPatch
	MonkeyPatch.patch_fromisoformat()


import hmac
import logging

import config
from mqtt import Mqtt
from common.validator import Validator
from interpreter import Interpreter
from status import StatusManager

logging.basicConfig(level=logging.DEBUG)

def close_door(door_name):
	print('close',door_name)
	mqtt.send(door_name,{'type':'close'})

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

def publish_status(status_manager):
	print("publish status",status_manager.status)
	mqtt.simple_send("doors/status",status_manager.status,retain=True)
	mqtt.simple_send("status/doorserver/public",status_manager.public,retain=True)
	mqtt.simple_send("status/doorserver/locked",not status_manager.open,retain=True)
	mqtt.simple_send("status/doorserver/occupied",status_manager.occupied,retain=True)

hmac_calculator=hmac.new(config.hmac_key,digestmod='sha512')
validator=Validator(hmac_calculator)
status=StatusManager(on_change=publish_status)
interpreter=Interpreter(status_manager=status,open_door=open_door,close_door=close_door,alarm_door=alarm_door)
mqtt=Mqtt(addr=config.mqtt_broker,validator=validator,interpreter=interpreter,status_manager=status)
mqtt.start()

