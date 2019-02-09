import unittest
import datetime

import validator

class Mock_hmac:
	def __init__(self):
		self.val=b''
	def copy(self):
		return self
	def update(self,arg):
		if not type(arg) is bytes:
			raise TypeError("Bytes expected. Got '{}' which is a '{}'.".format(arg,type(arg)))
		self.val+=arg
	def hexdigest(self):
		return hex(self.val[0])[2:]

class TestValidator(unittest.TestCase):
	def setUp(self):
		self.cot=validator.Validator(hmac=Mock_hmac())
	
	def test_hmac_int(self):
		self.assertRaises(AttributeError,self.cot.calculate_hmac,5)

	def test_hmac_str(self):
		self.assertEqual(self.cot.calculate_hmac('abc'),'61')

	def test_check_no_json(self):
		result=self.cot.check(b'abc')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid json'))

	def test_check_no_hmac(self):
		result=self.cot.check(b'{"payload":"test"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid json'))

	def test_check_no_payload(self):
		result=self.cot.check(b'{"hmac":"test"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid json'))

	def test_check_wrong_hmac(self):
		result=self.cot.check(b'{"hmac":"62","payload":"aac"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid HMAC'))

	def test_check_payload_not_json(self):
		result=self.cot.check(b'{"hmac":"61","payload":"abc"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid payload'))

	def test_check_payload_no_datetime(self):
		result=self.cot.check(b'{"hmac":"7b","payload":"{\\"data\\":\\"test\\"}"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid datetime'))

	def test_check_payload_wrong_datetime(self):
		result=self.cot.check(b'{"hmac":"7b","payload":"{\\"data\\":\\"test\\",\\"datetime\\":\\"wrong_datetime\\"}"}')
		self.assertIsNone(result[0])
		self.assertTrue(result[1].startswith('Invalid datetime'))

	def test_check_ok(self):
		now=datetime.datetime.now(datetime.timezone.utc).isoformat().encode('utf8')
		result=self.cot.check(b'{"hmac":"7b","payload":"{\\"data\\":\\"test\\",\\"datetime\\":\\"'+now+b'\\"}"}')
		self.assertIsNone(result[1])
		self.assertIs(type(result[0]),dict)
		self.assertEqual(result[0]['data'],"test")




class TestCheckDatetime(unittest.TestCase):
	def test_no_string(self):
		self.assertFalse(validator.check_datetime(0))
		self.assertFalse(validator.check_datetime(None))

	def test_no_date(self):
		self.assertFalse(validator.check_datetime('asdf'))

	def test_no_timezone(self):
		now=datetime.datetime.now()
		self.assertFalse(validator.check_datetime(now.isoformat()))

	def test_now(self):
		now=datetime.datetime.now(datetime.timezone.utc)
		self.assertTrue(validator.check_datetime(now.isoformat()))

	def test_allowed_past(self):
		delta=datetime.timedelta(seconds=validator.GRACE_PERIOD-1)
		now=datetime.datetime.now(datetime.timezone.utc)-delta
		self.assertTrue(validator.check_datetime(now.isoformat()))

	def test_allowed_future(self):
		delta=datetime.timedelta(seconds=validator.GRACE_PERIOD-1)
		now=datetime.datetime.now(datetime.timezone.utc)+delta
		self.assertTrue(validator.check_datetime(now.isoformat()))

	def test_past(self):
		delta=datetime.timedelta(seconds=validator.GRACE_PERIOD+1)
		now=datetime.datetime.now(datetime.timezone.utc)-delta
		self.assertFalse(validator.check_datetime(now.isoformat()))

	def test_future(self):
		delta=datetime.timedelta(seconds=validator.GRACE_PERIOD+1)
		now=datetime.datetime.now(datetime.timezone.utc)+delta
		self.assertFalse(validator.check_datetime(now.isoformat()))
