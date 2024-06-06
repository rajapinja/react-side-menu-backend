from flask import Flask, render_template
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store active video call rooms
video_call_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start-call')
def handle_start_call():
    room_id = 'room-123'  # You can generate unique room IDs
    user_id = 'user-123'  # You can use the user's session ID or username

    join_room(room_id)
    
    if room_id not in video_call_rooms:
        video_call_rooms[room_id] = []

    video_call_rooms[room_id].append(user_id)

    if len(video_call_rooms[room_id]) == 2:
        caller_id = video_call_rooms[room_id][0]
        callee_id = video_call_rooms[room_id][1]
        
        # Notify the callee about the incoming call
        socketio.emit('incoming-call', {'caller_id': caller_id}, room=callee_id)

@socketio.on('accept-call')
def handle_accept_call(signal_data):
    user_id = 'user-123'  # You can use the user's session ID or username
    join_room(user_id)
    socketio.emit('signal', signal_data, room=user_id)

@socketio.on('message')
def handle_message(message):
    room_id = 'room-123'  # You can generate unique room IDs
    user_id = 'user-123'  # You can use the user's session ID or username
    socketio.emit('message', message, room=room_id, skip_sid=user_id)


socketio.run(app, debug=True, port=5002)  # Change the port to 5001

if __name__ == '__main__':
    socketio.run(app, debug=True)
