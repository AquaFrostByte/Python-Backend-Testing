from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from datetime import datetime
import os
import time
import uuid

app = Flask(__name__)

app.secret_key = "supersecretkey"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'docx', 'avi'}

# Initialize SocketIO
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

# Route for the file upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/pfpupload')
def pfpupload():
    return render_template('pfpupload.html')

# Background thread for sending time updates via WebSocket
def background_time_thread():
    while True:
        now = datetime.now().strftime('%H:%M:%S')
        socketio.emit('time_update', {'time': now}, broadcast=True)  # Broadcast to all clients
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Start the background thread to send time updates
    socketio.start_background_task(background_time_thread)

# Upload functionality
def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a unique filename using UUID to prevent conflicts
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the uploads folder
        file.save(file_path)
        
        # Emit the new profile picture URL to the client
        image_url = url_for('uploaded_file', filename=filename)
        flash('File successfully uploaded')
        return {'image_url': image_url}, 200
    
    flash('File type not allowed')
    return redirect(url_for('upload'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == "__main__":
    socketio.run(app, debug=True)
