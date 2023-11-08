from flask import Flask, request, jsonify

import graphene
from graphene import ObjectType, String, List, Int, Float

app = Flask(__name__)

class Dispositivo(graphene.ObjectType):
    id = graphene.Int()
    nome = graphene.String()
    codigo = graphene.String()
    marca = graphene.String()

class Query(graphene.ObjectType):
    dispositivos = List(Dispositivo, marca=graphene.String())

    def resolve_dispositivos(self, info, marca=None):
        if marca:
            # Aqui você irá colocar a logica de filtrar dispositivos por marca, retornando
            # todos os dispositivos que tiverem uma marca igual a passada
            # Exemplo de query:
            #    {
            #        dispositivos{
            #           nome
            #           }
            #   }
            return [Dispositivo(id=1, nome="nome_d", codigo="123", marca=marca)]
        # Aqui você irá colocar a logica para retornar todos os dispositivos
        # Exemplo de query:
        #    {
        #        dispositivos(marca: "nome da marca"){
        #           nome
        #           }
        #   }
        return [Dispositivo(id=2, nome="d", codigo="1234", marca="qualquer")]

schema = graphene.Schema(query=Query)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data= request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(debug=True)
