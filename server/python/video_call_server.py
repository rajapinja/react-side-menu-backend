import cv2
import base64
import eventlet
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Video capture from the webcam
video_capture = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('video_frame', {'frame': frame_bytes}, namespace='/video')
            eventlet.sleep(1 / 30)  # Limit frame rate to 30 FPS

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0', port=5000)
