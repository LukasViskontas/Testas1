from machine import Pin, I2C
from time import sleep
import BME280
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

ssid = 'Lukas1'
password = 'n7pcJuuDpcG68T'
mqtt_server = 'mqtt.tagai.xyz'
client_id = ubinascii.hexlify(machine.unique_id())

topic_temp = 'LukasTest/pirmas/test'
last_message = 0
message_interval = 5

Wssid = 'HUAWEI-B535-FF89'
Wpassword = 'internetas223'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(Wssid, Wpassword)

while station.isconnected() == False:
  pass

print('Connection successful')

def connect_mqtt():
  global client_id, mqtt_server
  #client = MQTTClient(client_id, mqtt_server)
  client = MQTTClient(client_id, mqtt_server, user = ssid, password = password)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  machine.reset()

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# ESP8266 - Pin assignment
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

while True:
  try:
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    # uncomment for temperature in Fahrenheit
    #temp = (bme.read_temperature()/100) * (9/5) + 32
    #temp = str(round(temp, 2)) + 'F'
    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)
    client.publish(topic_temp, temp)

    sleep(30)
  except OSError as e:
    restart_and_reconnect()
