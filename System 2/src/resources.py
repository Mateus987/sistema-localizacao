from flask import request
from flask_restful import Resource
from src import db, api
from src.models import Dispositivo, Localizacao

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

    def put(self, dispositivo_id):
        data = request.get_json()
        dispositivo = Dispositivo.query.get(dispositivo_id)
        if dispositivo:
            dispositivo.nome = data.get('nome', dispositivo.nome)
            dispositivo.codigo = data.get('codigo', dispositivo.codigo)
            dispositivo.marca = data.get('marca', dispositivo.marca)
            db.session.commit()
        else:
            return "Dispotivo não encontrado!"

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

        return {
            'id': new_localizacao.id,
            'id_dispositivo': data.get('id_dispositivo'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }

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

api.add_resource(DispositivoResource, '/dispositivo', '/dispositivo/<string:dispositivo_id>')
api.add_resource(HistoricoLocalizacaoResource, '/historico/<string:dispositivo_id>')
api.add_resource(LocalizacaoResource, '/localizacao')