import json
from flask import request, make_response, jsonify
from flask_restful import Resource
from src import db, api
from src.models import Dispositivo, Localizacao
from src.redis import send_dict, get_valid_records
from websockets.sync.client import connect
from datetime import datetime

class DispositivoResource(Resource):
    def get(self, id_dispositivo):
        dispositivo = Dispositivo.query.get(id_dispositivo)
        if dispositivo:
            return {
                'id': dispositivo.id,
                'nome': dispositivo.nome,
                'codigo': dispositivo.codigo,
                'marca': dispositivo.marca
            }
        return {"message": "Dispositivo não encontrado"}, 404

    def post(self):
        data = request.get_json()

        new_dispositivo = Dispositivo(
                nome=data.get('nome'),
                codigo=data.get('codigo'),
                marca=data.get('marca')
            )
        db.session.add(new_dispositivo)
        db.session.commit()

        return {
            'id': new_dispositivo.id,
            'nome': data.get('nome'),
            'codigo': data.get('codigo'),
            'marca': data.get('marca')
        }

    def put(self, id_dispositivo):
        data = request.get_json()
        dispositivo = Dispositivo.query.get(id_dispositivo)
        if dispositivo:
            dispositivo.nome = data.get('nome', dispositivo.nome)
            dispositivo.codigo = data.get('codigo', dispositivo.codigo)
            dispositivo.marca = data.get('marca', dispositivo.marca)
            db.session.commit()
        else:
            return "Dispotivo não encontrado!"

        return {
            'id': id_dispositivo,
            'nome': data.get('nome'),
            'codigo': data.get('codigo'),
            'marca': data.get('marca')
        }

    def delete(self, id_dispositivo):
        dispositivo = Dispositivo.query.get(id_dispositivo)
        if dispositivo:
            db.session.delete(dispositivo)
            db.session.commit()
            return {"message": "Dispositivo removido com sucesso"}
        return {"message": "Dispositivo não encontrado"}, 404

class LocalizacaoResource(Resource):
    def post(self):
        data = request.get_json()

        new_localizacao = Localizacao(
                id_dispositivo=data.get('id_dispositivo'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
        db.session.add(new_localizacao)
        db.session.commit()

        dispositivo = Dispositivo.query.get(new_localizacao.id_dispositivo)

        data = {"id_dispositivo" : dispositivo.id
                ,"id_localizacao" : new_localizacao.id
                ,"latitude" : new_localizacao.latitude
                ,"longitude" : new_localizacao.longitude
                ,"data" : datetime.now()
            }

        # REDIS
        send_dict(data)

        del data["id_localizacao"]
        del data["data"]

        # WEB SOCKET
        with connect("ws://localhost:8765") as websocket:
            websocket.send(json.dumps(data))

        return {
            'id': new_localizacao.id,
            'id_dispositivo': data.get('id_dispositivo'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }

class HistoricoLocalizacaoResource(Resource):
    def get(self, id_dispositivo):
        try:
            return get_valid_records(id_dispositivo)
        except Exception:
            return make_response(jsonify("Internal Server Error")), 500

api.add_resource(DispositivoResource, '/dispositivo', '/dispositivo/<string:id_dispositivo>')
api.add_resource(HistoricoLocalizacaoResource, '/historico/<string:id_dispositivo>')
api.add_resource(LocalizacaoResource, '/localizacao')