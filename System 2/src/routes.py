from flask import make_response, jsonify
from src import app

@app.route("/")
def raiz():
    return make_response(jsonify({"Mensagem" : "Api esta funcionando!"})), 200