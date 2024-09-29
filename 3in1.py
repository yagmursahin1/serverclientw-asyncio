import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import socketio
import asyncio
from ultralytics import YOLO

sio = socketio.AsyncClient()

model=YOLO("/Users/yagmursahin/Desktop/allpython/newproject/best2.pt")
red=[0,0,255]

async def send_video():
    cap = cv2.VideoCapture(0)
    fps = 5
    interval = int(cap.get(cv2.CAP_PROP_FPS) / fps)
    frame_count = 0
    

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results=model(frame)
        for result in results:
            annotated_frame=result.plot()



        if frame_count % interval == 0:
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_to_send = BytesIO(buffer).getvalue()
            await sio.emit('video_frame', frame_to_send)

        cv2.imshow('Client1 - Sending Video', annotated_frame)
        if cv2.waitKey(1) == 27:
            break

        frame_count += 1
        await asyncio.sleep(0)

    cap.release()
    cv2.destroyAllWindows()

@sio.event
async def servo(data):
    print('servo açıldı')

async def main():
    await sio.connect('http://localhost:8081')
    await send_video()

asyncio.run(main())
