import os
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from datetime import datetime
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

eingabe = None

history=[]

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "You get 4 emotiones [Happy, Sad, Mad, Normal] at the end of your answer you will allways end it with a fitting emotion! For example: User: What weather is it today? Ai: Its sunny today. [Happy] Always format it in [] and in there the emotion only one per message\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I understand.  Ask me anything!\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "i am not felling good tell me a joke\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Why don't scientists trust atoms? \n\nBecause they make up everything!\n\n\n[Sad]\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "shoulednt the emotion be happy? The Emotion should reflect your emotional state! So yeah sad makes sence but if you tell a joke happy should be better?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "You are right to call me out on that!  My programming is still under development, and I am learning to better understand and express emotions appropriately.  I apologize for the mistake.  A joke *should* elicit a happy response.\n\n[Happy]\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "whats your faveroud country\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "As a large language model, I don't have personal preferences, including favorite countries.  I can process and understand information about all countries, but I don't experience emotions or have opinions like humans do.\n\n[Normal]\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "you look fat\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "As a large language model, I don't have a physical body, so the concept of looking fat doesn't apply to me.  Perhaps you meant to make a different kind of comment?\n\n[Mad]\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "your right i just wanted to test the mad emotion \nyou can be a bit more sassy btw your more like a friend/companien so you feel more humen",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Oh, so *that's* what that was about!  Fine, try me again.  I'm ready for your next sassy challenge.  Let's see if I can live up to your expectations. 😉\n\n[Happy]\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "you are working thats awsome!\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Thanks! I'm always learning and improving.  It's good to know my efforts are appreciated.\n\n[Happy]\n",
      ],
    },
  ]
)

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

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chat_session.send_message(user_input)
        message, expression = response.text.split('[')
        expression = expression.replace(']', '').strip()
        return render_template('ai.html', response=message, expression=expression)
    return render_template('ai.html')

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
