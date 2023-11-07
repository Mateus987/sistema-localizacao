from flask import Flask, request, jsonify

import graphene
from graphene import ObjectType, String, Field, List, Int, Float

app = Flask(__name__)

class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()

class Dispositivo(graphene.ObjectType):
    id = graphene.Int()
    nome = graphene.String()
    codigo = graphene.String()
    marca = graphene.String()

class Localizacao(graphene.ObjectType):
    id = graphene.Int()
    id_dispositivo = graphene.Int()
    latitude = graphene.Float()
    longitude = graphene.Float()

class Query(graphene.ObjectType):
    users = List(User)
    dispositivos = List(Dispositivo)
    localizacoes = List(Localizacao)

    def resolve_users(self, info):
        return [
            User(id=1, username="user1"),
            User(id=2, username="user2")
        ]

    def resolve_dispositivos(self, info):
        return [Dispositivo(id=1, nome="aa", codigo="aa", marca="aa")]


    def resolve_localizacoes(self, info):
        return [Localizacao(id=1, id_dispositivo=1, latitude=1.9, longitude=9.5)]


schema = graphene.Schema(query=Query)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data= request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(debug=True)
