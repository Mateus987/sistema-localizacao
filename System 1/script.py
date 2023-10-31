import time
import random
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código de resultado " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect("mqtt.broker.com", 1883, 60)  # Substitua mqtt.broker.com pelo seu broker MQTT

while True:
    device_id = "device123"
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    payload = '{{"device_id": "{}", "latitude": {}, "longitude": {}}}'.format(device_id, latitude, longitude)
    client.publish("localizacao", payload=payload, qos=1)
    print("Dados enviados: {}".format(payload))
    time.sleep(3)