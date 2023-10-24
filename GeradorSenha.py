import requests
import random
import sys


api_endpoint = "https://api.com/api/"


def gerar_coordenadas():
    latitude = random.uniform(-90, 90)  
    longitude = random.uniform(-180, 180) 
    return latitude, longitude

while True:

    latitude, longitude = gerar_coordenadas()

    id_ = random.randint(1, 5)

    url = f"{api_endpoint}{id_}/{latitude}/{longitude}"

    response = requests.post(url)

    if response.status_code == 200:
        print(f"Coordenadas ({latitude}, {longitude}) enviadas com sucesso para a API.")
    else:
        print("Erro ao enviar coordenadas para a API.")

    try:
        input("Pressione Enter para continuar ou Ctrl+C para sair...")
    except KeyboardInterrupt:
        print("Script interrompido manualmente.")
        sys.exit()
