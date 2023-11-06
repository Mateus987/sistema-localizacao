import time
import random
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='localizacao')

while True:
    id_dispositivo = "1cd68ad2-723f-4928-8213-a07dc517b84a"
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    payload = '{{"id_dispositivo": "{}", "latitude": {}, "longitude": {}}}'.format(id_dispositivo, latitude, longitude)
    channel.basic_publish("", "localizacao", payload)
    print(f"Dados enviados: {payload}")
    time.sleep(30)
