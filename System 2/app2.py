from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
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

@app.route("/")
def raiz():
    return make_response(jsonify({"Mensagem" : "Api esta funcionando!"})), 200

if __name__ == "__main__":
    app.run("127.0.0.1", 3333, False)