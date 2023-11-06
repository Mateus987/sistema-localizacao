from flask_socketio import emit
from src.models import Localizacao, Dispositivo

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