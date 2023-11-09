@echo off

echo "Inicializando Sistema 1"
start py ".\System 1\script.py"
start py ".\System 1\api.py"

echo "Incialize o REDIS"
pause

echo "Inicializando Sistema 2"
start py ".\System 2\api.py"
start py ".\System 2\web_socket.py"
start py ".\System 2\consume_queue.py"

echo "Inicializando o Sistema 3"
start node ".\System 3\grpc_server.js"
start node ".\System 3\web_socket_client.js"
start node ".\System 3\graph_ql.js"
start node ".\System 3\expurgo.js"

echo "Todos os sistemas inicializado!"

pause