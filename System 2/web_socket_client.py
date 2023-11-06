# Por hora isso é só pra representar o web socket client que vai ter no sistema 3

from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websocket:
        # websocket.send("Hello world!")
        while True:
            message = websocket.recv()
            print(f"Received: {message}")

hello()