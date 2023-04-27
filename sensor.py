import time
from grovepi import *
import grovepi

def set_bus(bus):
	global i2c
	i2c = di_i2c.DI_I2C(bus = bus, address = address)

address = 0x04
max_recv_size = 10
set_bus("RPI_1SW")

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# Connect the Grove Button to digital port D2
# SIG,NC,VCC,GND
led = 2

pinMode(led,"OUTPUT")

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")
time.sleep(1)
# Reference voltage of ADC is 5v
adc_ref = 5
# Vcc of the grove interface is normally 5v
grove_vcc = 5
# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

# analogRead() command format header
aRead_cmd = [3]

def write_i2c_block(block, custom_timing = None):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	counter = 0
	reg = block[0]
	data = block[1:]
	while counter < 3:
		try:
			i2c.write_reg_list(reg, data)
			time.sleep(0.002 + additional_waiting)
			return
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			continue
			
# Read I2C block from the GrovePi
def read_i2c_block(no_bytes = max_recv_size):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	data = data_not_available_cmd
	counter = 0
	while data[0] in [data_not_available_cmd[0], 255] and counter < 3:
		try:
			data = i2c.read_list(reg = None, len = no_bytes)
			time.sleep(0.002 + additional_waiting)
			if counter > 0:
				counter = 0
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			
	return data

def read_identified_i2c_block(read_command_id, no_bytes):
	data = [-1]
	while len(data) <= 1:
		data = read_i2c_block(no_bytes + 1)

	return data[1:]

# Read analog value from Pin
def analogRead(pin):
	write_i2c_block(aRead_cmd + [pin, unused, unused])
	number = read_identified_i2c_block(aRead_cmd, no_bytes = 2)
	return number[0] * 256 + number[1]


CODE = {' ': ' ', 
        "'": '.----.', 
        '(': '-.--.-', 
        ')': '-.--.-', 
        ',': '--..--', 
        '-': '-....-', 
        '.': '.-.-.-', 
        '/': '-..-.', 
        '0': '-----', 
        '1': '.----', 
        '2': '..---', 
        '3': '...--', 
        '4': '....-', 
        '5': '.....', 
        '6': '-....', 
        '7': '--...', 
        '8': '---..', 
        '9': '----.', 
        ':': '---...', 
        ';': '-.-.-.', 
        '?': '..--..', 
        'A': '.-', 
        'B': '-...', 
        'C': '-.-.', 
        'D': '-..', 
        'E': '.', 
        'F': '..-.', 
        'G': '--.', 
        'H': '....', 
        'I': '..', 
        'J': '.---', 
        'K': '-.-', 
        'L': '.-..', 
        'M': '--', 
        'N': '-.', 
        'O': '---', 
        'P': '.--.', 
        'Q': '--.-', 
        'R': '.-.', 
        'S': '...', 
        'T': '-', 
        'U': '..-', 
        'V': '...-', 
        'W': '.--', 
        'X': '-..-', 
        'Y': '-.--', 
        'Z': '--..', 
        '_': '..--.-'}
        
import paho.mqtt.client as mqtt #import library
 
MQTT_SERVER = "172.20.10.12" #specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PATH = "data" #this is the name of topic, like temp

speed = grovepi.analogRead(potentiometer)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if str(msg.payload) == "speed":
    	print("Make your speed adjustment right now!")
    	time.sleep(5)
    	speed = grovepi.analogRead(potentiometer)
    else:
    	print("The message is: " + str(msg.payload))
    	speed = grovepi.analogRead(potentiometer)
    	print("Currently the speed is: " + str(speed))
    	process_morse(str(msg.payload))
    	print("Finished conversion process")
    
def blink():
    digitalWrite(led,1)     # Send HIGH to switch on LED
    time.sleep(float(speed)/750.0)

    digitalWrite(led,0)     # Send LOW to switch off LED
    time.sleep(float(speed)/750.0)
    
def blonk():
    digitalWrite(led,1)     # Send HIGH to switch on LED
    time.sleep(float(speed)/750.0 + 1)

    digitalWrite(led,0)     # Send LOW to switch off LED
    time.sleep(float(speed)/750.0 + 1)
    
    
def process_morse(msg):
    for letter in msg.upper():
    	to_process = CODE[letter]
    	for morse in to_process:
    		if morse == '.':
    			blink()
    		else:
    			blonk()
    	time.sleep(float(speed)/750.0 + 2)
    
   
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)

client.loop_forever()
	
