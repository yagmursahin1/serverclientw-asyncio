import socketio
import cv2
import numpy as np
from io import BytesIO
import threading

sio = socketio.SimpleClient()

sio.connect('http://localhost:8081')

def video_frame(data: list):
    video_bytes = data[1]
    video_stream = BytesIO(video_bytes)
    nparr = np.frombuffer(video_stream.getvalue(), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is not None:
        cv2.imshow('Client2 - Receiving Video', frame)
        if cv2.waitKey(1) == 27:           
            cv2.destroyAllWindows()
            sio.disconnect()
    else:
        print("Failed to decode frame")
        return

def servo():
    sio.emit('servo',{'message':'servo'})
    print('Servo signal sent')

def handle_input():
    while True:
        key=input("Press 's' to send servo signal: ")
        if key == 's':
            servo()
        elif key == 'q':
            break

thr=threading.Thread(target=handle_input)
thr.start() 

while True:
    data:list=sio.receive()
    if data[0]=="video_frame":
        video_frame(data)
    else:
        print("Gelen data video_frame değil")
    if cv2.waitKey(1)==27:
        break
    
thr.join()
cv2.destroyAllWindows()
sio.disconnect()
