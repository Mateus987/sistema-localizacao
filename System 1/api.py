from flask import Flask, request
import pika

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Substitua localhost pelo seu servidor RabbitMQ
channel = connection.channel()
channel.queue_declare(queue='localizacao_queue')

def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")
    channel.basic_publish(exchange='', routing_key='localizacao_queue', body=data)
    print("Dados recebidos via MQTT e encaminhados para a fila: {}".format(data))

app.run(host='0.0.0.0', port=5000)  # A API estará acessível em http://localhost:5000