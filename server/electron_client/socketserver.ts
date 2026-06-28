import * as http from 'http'
const wss = new http.Server();

wss.listen(3000, () => {
  console.log('WebSocket server listening on port 3000');
});

wss.on('connection', (ws: any) => {
  console.log('Client connected');

  ws.on('message', (message: any) => {
    console.log(`Received message: ${message}`);
    ws.send(`Server received your message: ${message}`);
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

