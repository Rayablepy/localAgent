import asyncio
import json
import socketio
sio = socketio.AsyncClient()
def requestparser(data):
    if isinstance(data, str):
        return json.loads(data)
    return data
def responseparser(data):
    return json.dumps(data)

@sio.event
async def connect():
    print('connected')

@sio.on('transmit-data')
async def receive_request(data):
    try:
        parsed = requestparser(data)
        print(f"Received: {parsed}")
    except json.JSONDecodeError:
        print('error parsing json request')

@sio.on('response')
async def transmit_response(data):
    try:
        parsed = requestparser(data)
        print(f"Response: {parsed}")
    except json.JSONDecodeError:
        print(f"failed to decode non json response: {data}")
@sio.event
async def disconnect():
    print('disconnected')

async def send_messages():
    while True:
        raw = await asyncio.to_thread(input, "send json")
        try:
            py_data = json.loads(raw)
        except json.JSONDecodeError:
            print('error parsing json')
            continue
        json_data = responseparser(py_data)
        await sio.emit('transmit-data', json_data)
async def main():
    await sio.connect('http://localhost:3000')
    transmitter = asyncio.create_task(send_messages())
    try:
        await sio.wait()
    finally:
        transmitter.cancel()

asyncio.run(main())
