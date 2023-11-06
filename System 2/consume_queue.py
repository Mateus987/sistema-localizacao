import json
import pika
import time
import requests

def get_elements_in_queue(ch, method, properties, body):
    element = json.loads(body.decode("utf-8"))
    print(f"Queue: {method.routing_key}, Mensagem: {element}")
    for n_try in range(3):
        try:
            req = requests.post("http://localhost:3333/localizacao", json=element)
            if req.status_code != 200:
                print(f"Erro ao salvar dados no banco\nStatus Code: {req.status_code}\nMessage: {req.json()}")
                time.sleep(3)
                continue
            else:
                print("Localização salva no banco de dados:", element)
                break
        except Exception as e:
            print("Erro ao fazer requisição na API:", e)
            time.sleep(3)
            continue


def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    queue_name = "localizacao_queue"
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=get_elements_in_queue, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    consume_queue()