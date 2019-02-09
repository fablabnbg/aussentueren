import pin

import unittest


class TestPin(unittest.TestCase):
	def test_is_pin_too_short(self):
		self.assertFalse(pin.is_pin('123'))

	def test_is_pin_too_long(self):
		self.assertFalse(pin.is_pin('12345'))

	def test_is_pin_no_string(self):
		self.assertRaises(TypeError,pin.is_pin,123)

	def test_is_pin_no_numbers(self):
		self.assertFalse(pin.is_pin('abc'))

	def test_is_pin_correct(self):
		self.assertTrue(pin.is_pin('1234'))


	def test_pin_change_correct(self):
		result=pin.is_pin_change("*0000#1111#1111#")
		self.assertEqual(result['oldpin'],'0000')
		self.assertEqual(result['newpin'],'1111')

	def test_pin_change_pins_not_same(self):
		self.assertIsNone(pin.is_pin_change("*0000#1011#1111#"))

	def test_pin_change_new_pin_too_short(self):
		self.assertIsNone(pin.is_pin_change("*0000#111#111#"))

	def test_pin_change_new_pin_letters(self):
		self.assertIsNone(pin.is_pin_change("*0000#111a#111a#"))

	def test_pin_change_new_pin_oly_once(self):
		self.assertIsNone(pin.is_pin_change("*0000#1111#"))

	def test_pin_change_new_pin_too_long(self):
		self.assertIsNone(pin.is_pin_change("*0000#11111#11111#"))
