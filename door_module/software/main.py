#!/usr/bin/env python3
import lock_ctrl
from  IOctrl import gpio
import NFCreader
from door import Door
import datetime
import config
from keypad import Keypad
from identity_store import Identity_store
import pin
import beeper
from interpreter import Interpreter
from mqtt import Mqtt
from common.validator import Validator
import hmac
import logging
import serial

from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()

logging.basicConfig(level=logging.DEBUG)

def card_on_door(ident,sak):
	ident=ident.decode('utf8')
	sak=sak.decode('utf8')
	logging.info('Card at outside reader "{}"'.format(ident))
	keypad.flush()
	if door.is_closed:
		ident_store.uid=ident
		ident_store.sak=sak
	beep_door.confirm()
	mqtt.send('card_shown_outside',{'card':ident,'sak':sak})

def card_on_exit(ident,sak):
	ident=ident.decode('utf8')
	logging.info('Card at inside reader "{}"'.format(ident))
	beep_exit.confirm()
	mqtt.send('card_shown_inside',{'card':ident,'sak':sak.decode('utf8')})

def on_door_open():
	ident_store.uid=None
	mqtt.send('open',{'status':True},retain=True)

def on_door_close():
	ident_store.uid=None
	mqtt.send('open',{'status':False},retain=True)

def on_key(buf):
	beep_door.running=False
	beep_door.keypress()
	uid=ident_store.uid
	sak=ident_store.sak
	if not uid:
		return
	if pin.is_pin(buf):
		mqtt.send('card_shown_outside',{'card':uid,'sak':sak,'pin':buf})
	pin_change=pin.is_pin_change(buf)
	if pin_change:
		old_pin=pin_change['oldpin']
		new_pin=pin_change['newpin']
		mqtt.send('change_pin',{'card':uid,'sak':sak,'old_pin':old_pin,'new_pin':new_pin})

ident_store=Identity_store()
door=Door(gpio(config.gpio_door_sensor),open_callback=on_door_open,close_callback=on_door_close)
lock_control=lock_ctrl.Lock_ctrl(IO_latch=gpio(config.gpio_electric_strike),IO_closer=gpio(config.gpio_door_closer))

keypad=Keypad(dev=serial.Serial(config.keypad_dev,9600),on_key=on_key)
keypad.start()

reader_door=NFCreader.NFCreader(dev=config.outside_reader_dev,on_card=card_on_door)
reader_exit=NFCreader.NFCreader(dev=config.inside_reader_dev,on_card=card_on_exit)
beep_door=beeper.Beeper(reader_door.beep)
beep_exit=beeper.Beeper(reader_exit.beep)

interpreter=Interpreter(opener=lock_control.latch,public=lock_control.public,beeper_inside=beep_exit.beep_by_style,beeper_outside=beep_door.beep_by_style)
hmac_calculator=hmac.new(config.hmac_key,digestmod='sha512')
validator=Validator(hmac_calculator)
mqtt=Mqtt(addr=config.mqtt_broker,name=config.door_name,validator=validator,interpreter=interpreter)

reader_exit.start()
reader_door.start()
logging.info('Started at {}'.format(datetime.datetime.now().isoformat()))
