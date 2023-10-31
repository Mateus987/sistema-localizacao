from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
import json
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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

mqtt_broker_address = "seu-broker-mqtt.com"
mqtt_port = 1883
mqtt_topic = "topic/para/enviar/coordenadas"

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    id_dispositivo = payload["id"]
    latitude = payload["latitude"]
    longitude = payload["longitude"]

    nova_localizacao = Localizacao(id_dispositivo=id_dispositivo, latitude=latitude, longitude=longitude)
    db.session.add(nova_localizacao)
    db.session.commit()
    
    print(f"Nova localização recebida e adicionada ao banco de dados:")
    print("ID do Dispositivo:", id_dispositivo)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("-----------------------")


mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message


mqtt_client.connect(mqtt_broker_address, mqtt_port, 60)

mqtt_client.subscribe(mqtt_topic)


if __name__ == '__main__':
    db.create_all()
    mqtt_client.loop_start()  
    app.run(debug=True)
