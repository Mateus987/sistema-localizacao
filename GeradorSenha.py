import requests
import random
import paho.mqtt.client as mqtt
import json
import time


mqtt_broker_address = "seu-broker-mqtt.com"
mqtt_port = 1883
mqtt_topic = "topic/para/enviar/coordenadas"


def gerar_coordenadas():
    latitude = random.uniform(-90, 90) 
    longitude = random.uniform(-180, 180) 
    return latitude, longitude

def on_connect(client, userdata, flags, rc):
    print("Conectado ao MQTT Broker com código de resultado " + str(rc))

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect


mqtt_client.connect(mqtt_broker_address, mqtt_port, 60)


while True:
  
    latitude, longitude = gerar_coordenadas()


    id_ = random.randint(1, 5)

  
    payload = {
        "id": id_,
        "latitude": latitude,
        "longitude": longitude
    }

  
    payload_json = json.dumps(payload)

  
    mqtt_client.publish(mqtt_topic, payload_json)

    print(f"Coordenadas ({latitude}, {longitude}) enviadas via MQTT para o tópico '{mqtt_topic}'.")

