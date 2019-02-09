import dotenv
import os
dotenv.load_dotenv()

gpio_door_sensor=os.getenv('GPIO_DOOR_SENSOR')
gpio_electric_strike=os.getenv('GPIO_DOOR_SENSOR')
hmac_key=os.getenv('HMAC_KEY').encode('utf8')
mqtt_broker=os.getenv('MQTT_BROKER')
door_name=os.getenv('DOOR_NAME')
outside_reader_dev=os.getenv('OUTSIDE_READER_DEV')
inside_reader_dev=os.getenv('INSIDE_READER_DEV')
keypad_dev=os.getenv('KEYPAD_DEV')
