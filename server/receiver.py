import asyncio
import socketio
sio = socketio.AsyncClient()
@sio.event
async def connect():
    print('connected')

@sio.event
async def transmit_data(data):
    await sio.emit('transmit-data', data)

@sio.event
async def disconnect():
    print('disconnected')

async def main():
    await sio.connect('http://localhost:3000')
    await sio.wait()

asyncio.run(main())
