const ws = new WebSocket('ws://localhost:8765');

ws.addEventListener('open', () => {
  console.log('Connected to WebSocket server');
});

ws.addEventListener('message', (event) => {
  console.log(`Received: ${event.data}`);
  message = JSON.parse(event.data);

  updateLayout(`${message.latitude.toFixed(2)} | ${message.longitude.toFixed(2)}`);
});

function updateLayout(message) {
  const messageContainer = document.getElementById('ultima_pos');
  messageContainer.innerHTML = message;
}