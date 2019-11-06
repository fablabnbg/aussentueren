from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, func, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
#from pytz import utc

import json

Base=declarative_base()

class Card(Base):
	__tablename__='cards'
	uid=Column(String(14),primary_key=True)
	pin=Column(String(4))
	owner=Column(String(64),nullable=True)
	member_id=Column(String(5))
	expiry_date=Column(Date)
	allow_unlock=Column(Boolean,default=False,nullable=False)
	allow_entry=Column(Boolean,default=False,nullable=False)
	allow_sneaky=Column(Boolean,default=False,nullable=False)
	always_sneaky=Column(Boolean,default=False,nullable=False)

class Door(Base):
	__tablename__='doors'
	name=Column(String(16),primary_key=True)

class Request_Success(Base):
	__tablename__='requests_success'
	id=Column(Integer,primary_key=True)
	date=Column(DateTime, default=func.now())
	card_uid=Column(String(14))
	req_type=Column(Enum('open','close'))
	door_name=Column(String(16),ForeignKey('doors.name'))
	door=relationship(Door)

class Request_Failure(Base):
	__tablename__='requests_failure'
	id=Column(Integer,primary_key=True)
	date=Column(DateTime, default=func.now())
	card_uid=Column(String(14))
	req_type=Column(Enum('open','close'))
	door_name=Column(String(16),ForeignKey('doors.name'))
	door=relationship(Door)

class Alarm(Base):
	__tablename__='alarms'
	id=Column(Integer,primary_key=True)
	date=Column(DateTime, default=func.now())
	type=Column(String(32))
	door_name=Column(String(16),ForeignKey('doors.name'))
	door=relationship(Door)

	def __str__(self):
		#return '"{}" from "{}" on "{}"'.format(self.type,self.door.name,utc.localize(self.date))
		return '"{}" from "{}" on "{}"'.format(self.type,self.door.name,self.date)

def create_tables(dbengine):
	__engine=create_engine(dbengine)
	Base.metadata.create_all(__engine)

def create_session(dbengine):
	__engine=create_engine(dbengine)
	Session=sessionmaker(bind=__engine)
	return Session()
