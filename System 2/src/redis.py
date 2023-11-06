from src import r
from datetime import datetime, timedelta

def send_dict(data):
    ttl = timedelta(hours=24)
    name = f"disp_loc:{data['id_dispositivo']}:{data['id_localizacao']}"
    r.hset(name=name, mapping=data)
    r.expire(name=name, time=ttl)

def get_valid_records(id_dispositivo):
    valid_records = []
    all_keys = r.keys(f"disp_loc:{id_dispositivo}:*")  # Obtém todas as chaves relevantes

    for key in all_keys:
        remaining_time = r.ttl(key)
        if remaining_time > 0:
            # A chave ainda não expirou
            record = r.hgetall(key)
            valid_records.append(record)

    return valid_records
