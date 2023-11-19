import database as db
import config
#import config
#import json
import sqlalchemy.orm.exc as exc
#from app_status import get_status, send_status
from datetime import date
#import threading

class Interpreter:
	def __init__(self,status_manager,open_door,close_door,alarm_door):
		self.status_manager=status_manager
		self.open_door=open_door
		self.close_door=close_door
		self.alarm_door=alarm_door

	def do(self,door_name,request,data):
		if request=="card_shown_inside":
			self.close(door_name,data)
		elif request=="card_shown_outside":
			if not self.status_manager.public: # Ignore card if public mode
				self.open(door_name,data)
		elif request=="change_pin":
			self.change_pin(door_name,data)

	def do_public(self,status):
		self.status_manager.public=status.decode().upper()=="TRUE"

	def open(self,door_name,data):
		card_uid=data.get('card','')
		print('open with Card: "{}"'.format(card_uid))
		s=db.create_session(config.db)
		try:
			card=s.query(db.Card).filter(db.Card.uid==card_uid.upper()).one()
		except exc.NoResultFound:
			return self.fail_open(s,card_uid,door_name)
		if not card.allow_entry:
			return self.fail_open(s,card_uid,door_name)
		if self.status_manager.open:
			return self.grant_open(s,card_uid,door_name)
		if card.expiry_date is None or card.expiry_date<date.today():
			return self.fail_open(s,card_uid,door_name)
		if card.allow_unlock:
			pin=data.get('pin','no pin')
			sneaky=False
			if pin.startswith('#'):
				sneaky=True
				pin=pin[1:]
			if not card.allow_sneaky:
				sneaky=False
			if card.always_sneaky:
				sneaky=True
			if card.pin==pin:
				return self.grant_open(s,card_uid,door_name,sneaky)
			else:
				self.alarm_door(door_name,'pin')
				return
		return self.fail_open(s,card_uid,door_name)

	def close(self,door_name,data):
		card_uid=data.get('card','')
		self.status_manager.open=False
		self.status_manager.occupied=False
		self.status_manager.public=False
		self.alarm_door(door_name,'close')
		r=db.Request_Success(card_uid=card_uid,req_type='close',door_name=door_name)
		s=db.create_session(config.db)
		s.add(r)
		s.commit()


	def change_pin(self,door_name,data):
		card_uid=data.get('card','')
		old_pin=data.get('old_pin','')
		new_pin=data.get('new_pin','')
		s=db.create_session(config.db)
		try:
			card=s.query(db.Card).filter(db.Card.uid==card_uid.upper()).one()
		except exc.NoResultFound:
			self.alarm_door(door_name,'deny')
		if card.pin!=old_pin:
			self.alarm_door(door_name,'deny')
		if len(new_pin)!=len(old_pin):
			self.alarm_door(door_name,'deny')
		card.pin=new_pin
		s.merge(card)
		s.commit()
		self.alarm_door(door_name,'pin_changed')

	def grant_open(self,session,card_uid,door,sneaky=False):
		r=db.Request_Success(card_uid=card_uid,req_type='open',door_name=door)
		session.add(r)
		session.commit()
		self.open_door(door)
		is_open=self.status_manager.open or not sneaky
		self.status_manager.open=is_open
		self.status_manager.occupied=True

	def fail_open(self,session,card_uid,door):
		r=db.Request_Failure(card_uid=card_uid,req_type='open',door_name=door)
		session.add(r)
		session.commit()
		self.alarm_door(door,'deny')
