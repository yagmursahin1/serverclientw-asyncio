import socketio
import aiohttp
from aiohttp import web

sio=socketio.AsyncServer(async_mode='aiohttp')
app=web.Application()
sio.attach(app)

@sio.event
async def video_frame(sid,data):
       await sio.emit('video_frame',data,skip_sid=sid)

@sio.event
async def connect(sid,data,abc):
    print(f"{sid} connected")

@sio.event
async def servo(sid,data):
    await sio.emit('servo',data,skip_sid=sid)


if __name__=='__main__':
    web.run_app(app,port=8081)