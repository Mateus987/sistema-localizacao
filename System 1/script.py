import time
import random
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='localizacao')

while True:
    id_dispositivo = "cbda669f-2290-4e48-89d0-cae50e001441"
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    payload = '{{"id_dispositivo": "{}", "latitude": {}, "longitude": {}}}'.format(id_dispositivo, latitude, longitude)
    channel.basic_publish("", "localizacao", payload)
    print(f"Dados enviados: {payload}")
    time.sleep(30)
