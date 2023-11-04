from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
import uuid
import pika
import time
import threading

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dispositivo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    localizacoes = db.relationship('Localizacao', backref='dispositivo', lazy=True)

class Localizacao(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    id_dispositivo = db.Column(db.String(36), db.ForeignKey('dispositivo.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class DispositivoResource(Resource):
    def get(self, dispositivo_id):
        dispositivo = Dispositivo.query.get(dispositivo_id)
        if dispositivo:
            return {
                'id': dispositivo.id,
                'nome': dispositivo.nome,
                'codigo': dispositivo.codigo,
                'marca': dispositivo.marca
            }
        return {"message": "Dispositivo não encontrado"}, 404

    def put(self, dispositivo_id):
        data = request.get_json()
        dispositivo = Dispositivo.query.get(dispositivo_id)
        if dispositivo:
            dispositivo.nome = data.get('nome', dispositivo.nome)
            dispositivo.codigo = data.get('codigo', dispositivo.codigo)
            dispositivo.marca = data.get('marca', dispositivo.marca)
            db.session.commit()
        else:
            new_dispositivo = Dispositivo(
                id=dispositivo_id,
                nome=data.get('nome'),
                codigo=data.get('codigo'),
                marca=data.get('marca')
            )
            db.session.add(new_dispositivo)
            db.session.commit()

        return {
            'id': dispositivo_id,
            'nome': data.get('nome'),
            'codigo': data.get('codigo'),
            'marca': data.get('marca')
        }

    def delete(self, dispositivo_id):
        dispositivo = Dispositivo.query.get(dispositivo_id)
        if dispositivo:
            db.session.delete(dispositivo)
            db.session.commit()
            return {"message": "Dispositivo removido com sucesso"}
        return {"message": "Dispositivo não encontrado"}, 404

class HistoricoLocalizacaoResource(Resource):
    def get(self, dispositivo_id):
        localizacoes = Localizacao.query.filter_by(id_dispositivo=dispositivo_id).all()
        historico = []
        for localizacao in localizacoes:
            historico.append({
                'latitude': localizacao.latitude,
                'longitude': localizacao.longitude
            })
        return historico

api.add_resource(DispositivoResource, '/dispositivo/<string:dispositivo_id>')
api.add_resource(HistoricoLocalizacaoResource, '/historico/<string:dispositivo_id>')


def enviar_ultima_localizacao(dispositivo_id):
    localizacao = Localizacao.query.filter_by(id_dispositivo=dispositivo_id).order_by(Localizacao.id.desc()).first()
    if localizacao:
        emit('update_location', {
            'latitude': localizacao.latitude,
            'longitude': localizacao.longitude
        })

import time

def atualizar_localizacao_em_tempo_real():
    while True:
        dispositivos_ids = [dispositivo.id for dispositivo in Dispositivo.query.all()]
        for dispositivo_id in dispositivos_ids:
            enviar_ultima_localizacao(dispositivo_id)
        time.sleep(1)

@app.route("/")
def raiz():
    return make_response(jsonify({"Mensagem" : "Api esta funcionando!"})), 200

def get_elements_in_queue(ch, method, properties, body):
    element = json.loads(body.decode("utf-8"))
    # TODO: criar a logica para inserir o element dentro do banco de dados
    print(f"Queue: {method.routing_key}, Mensagem: {element['longitude']}")

def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    queue_name = "localizacao_queue"
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=get_elements_in_queue, auto_ack=True)
    channel.start_consuming()

def init_server():
    app.run("127.0.0.1", 3333, False)

thread1 = threading.Thread(target=init_server)
thread2 = threading.Thread(target=consume_queue)

if __name__ == "__main__":
    # TODO: melhorar esse sistema de threads, pois foi improvissado para que ambos os sistemas rodassem juntos
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
"""
API de Rastreio
- Um banco de dados
- Com cache Redis
- REST
- E essa api fornece dados para o front end por meio de um web socket
"""