from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import time

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def background_time_thread():
    while True:
        now = datetime.now().strftime('%H:%M:%S')
        socketio.emit('time_update', {'time': now})
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Start the background thread to send time updates
    socketio.start_background_task(background_time_thread)

if __name__ == '__main__':
    socketio.run(app, debug=True)
