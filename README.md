# Sistema de Localizacao

### Setup:

* Instalar os pacotes python dos requirements.txt de cada System
```pip install -r requirements.txt```

* Instalar o erlang: https://www.erlang.org/downloads

* Instalar o Rabbit MQ: https://www.rabbitmq.com/download.html

* Instalar o Windows Subsystem for Linux: https://learn.microsoft.com/en-us/windows/wsl/install

Esse cara é basicamente rodar um ```wsl --install```, se seu PC for compativel ele vai instalar tudo, ai é só reiniciar e terminar a configuração do usuário Linux

* Linha que gera os arquivos do GRPC no python: ```python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. your_service.proto```

### Docs:
* Flask: https://flask.palletsprojects.com/en/2.3.x/
* Rabbit MQ: https://www.rabbitmq.com/documentation.html
* Redis: https://redis.io/docs/connect/clients/python/

### System 1
* Script - Gera localizações para x dispositivo e envia elas pra queue "localizacao" do Rabit MQ
* Api - Consome essa queue "localizacao" e envia ela para a queue "localizacao_queue", que vai ser consumida pela API Rest

### System 2
API Restful em Flask
- Recebe essa localizacao da queue do rabbit MQ
- Salva essa localização no banco de dados
- No redis:
  - Tem que salvar as localizações que entram nele com duração de 1 dia, para poder usar no histórico das ultimas 24 horas
- CRUD dos dispositivos salvos no banco (essa crud vai consumida principalmente pelo front do System 1)
- Web Socket que envia a ultima localização

### System 3
API de Metricas
- Recebe os dispositivos registrados na API por GRPC
- Recebe todas as localizações registradas na API por Web Socket, e com uma lógica salva as infos desse dispositivo aqui
- Graph QL é usado para fazer buscas no banco local dessa aplicação
- Front end com as metricas e ultimas posições

### TODO
* Sistema 3
  - Graph QL
  - Fazer o front
* Padronização com Pylint
