from src import app

if __name__ == "__main__":
    app.run("127.0.0.1", 3333, False)

"""
API de Rastreio
- Um banco de dados
- Com cache Redis
- REST
- E essa api fornece dados para o front end por meio de um web socket
"""