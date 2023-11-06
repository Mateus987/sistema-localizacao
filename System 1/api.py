import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='localizacao')
channel.queue_declare(queue='localizacao_queue')

def on_message(ch, method, properties, body):
    data = body.decode("utf-8")
    channel.basic_publish(exchange='', routing_key='localizacao_queue', body=data)
    print("Dados recebidos via MQTT e encaminhados para a fila: {}".format(data))

channel.basic_consume(queue="localizacao", auto_ack=True, on_message_callback=on_message)
channel.start_consuming()
