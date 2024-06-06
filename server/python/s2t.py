from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import io
from flask_cors import CORS
import speech_recognition as sr
import os
from werkzeug.utils import secure_filename  # Import secure_filename
import subprocess
import ffmpeg
import threading  # For creating a separate recording thread
import base64
import tempfile



app = Flask(__name__)
CORS(app)  # Enable CORS for your entire Flask app

recognizer = sr.Recognizer()

# Set audio parameters
sample_rate = 44100  # Example sample rate
bit_depth = 16       # Example bit depth
channels = 1         # Example number of channels (mono)

# Global variable to store the recorded audio
recorded_audio = None
is_recording = False

#sr version
print(sr.__version__)
recognizer.energy_threshold = 300

# Lock for thread synchronization
recording_lock = threading.Lock()

# Define a function to start recording
def start_recording():
    global is_recording
    global recorded_audio_base64
    if not is_recording:
        with recording_lock:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source, timeout=220)

            recorded_audio_base64 = base64.b64encode(audio.frame_data).decode('utf-8')
            is_recording = True
            return recorded_audio_base64

# Define a function to stop recording
def stop_recording():
    global is_recording
    global recorded_audio_base64
    if recorded_audio_base64:
        with recording_lock:
            audio_bytes = base64.b64decode(recorded_audio_base64)
            #with open("microphone-audio.wav", "wb") as f:
                # f.write(audio_bytes)
            with wave.open("microphone-audio.wav", "wb") as f:
                f.setnchannels(channels)
                f.setsampwidth(bit_depth // 8)
                f.setframerate(sample_rate)
                f.writeframes(audio_bytes)
        return {'message': 'Audio File Created Successfully..!'}
    else:
        return {'error': 'No recorded audio available.'}

# API route to start recording
@app.route('/api/microphone_start_recording', methods=['POST'])
def microphone_start_recording_api():
    try:
        global is_recording
        global recorded_audio_base64
        recorded_audio_base64 = None
        audio_base64 = start_recording()
        is_recording = True
        return jsonify({"response": audio_base64, "message": 'Recording started'})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': f'Error with the speech recognition service: {str(e)}'})

# API route to stop recording
@app.route('/api/microphone_stop_recording', methods=['POST'])
def microphone_stop_recording_api():
    try:
        global is_recording
        global recorded_audio_base64
        audio_response = stop_recording()
        is_recording = False
        return jsonify({'response': audio_response, "message": 'Stopped recording successfully..!'})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': f'Error with the speech recognition service: {str(e)}'})


@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text_api():
    # obtain audio from the microphone
    #r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = recognizer.listen(source)

    # write audio to a WAV file
    # with open("microphone-results.wav", "wb") as f:
    #     f.write(audio.get_wav_data())
    audio_file_1 = request.files['audio']

    # Ensure that the uploaded file has a valid name
    if not audio_file_1.filename:
        return jsonify({'error': 'Invalid audio file name'})

    audio_file_path = os.path.join('temp', secure_filename(audio_file_1.filename))

    # If the file is not in WAV format, convert it to WAV
    if not is_wav_file(audio_file_path):
        audio_file_path = convert_audio_to_wav(audio_file_1)

    # audio_file_ = sr.AudioFile(audio_file_path)
    # type(audio_file_)      

    try:
        if audio_file_path:
            with sr.AudioFile(audio_file_path) as source:
                audio_file = recognizer.record(source, duration=120)
                result = recognizer.recognize_google(audio_data=audio_file)
                print("result :", result)
                return jsonify({'result': result})  # Return recognized text                        
        else:
            return jsonify({'error': 'Failed to convert audio to WAV'})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': f'Error with the speech recognition service: {str(e)}'})  
    

#Convert Other audio files to .wav file
def convert_audio_to_wav(audio_file):
    # Define the path to ffmpeg.exe
    ffmpeg_path = r'C:\_Softwares\ffmpeg\bin\ffmpeg.exe'

    # Generate a secure filename for the audio file
    audio_filename = secure_filename(audio_file.filename)

    # Save the uploaded audio file temporarily
    temp_audio_path = os.path.join('temp', audio_filename)

    # Save the original audio file
    audio_file.save(temp_audio_path)

    # Construct the output file path (WAV format)
    wav_output_path = os.path.join('temp', audio_filename.rsplit('.', 1)[0] + '.wav')

    # Construct the command to convert the audio to WAV
    cmd = [
        ffmpeg_path,
        '-i', temp_audio_path,
        '-f', 'wav',
        '-y',  # Overwrite output if it exists
        wav_output_path  # Output file path
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Converted File :",wav_output_path)
        return wav_output_path
    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg:", e)
        return None
    finally:
        # Clean up temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

def is_wav_file(file_path):
    return os.path.splitext(file_path)[1].lower() == '.wav'

#Convert give text to Speech
@app.route('/api/convert_text_to_speech', methods=['POST'])
def convert_text_to_speech():

    text = request.json['text']    
    #print("text :", text);
    tts = gTTS(text)    
    #print("tts :", tts);
    # Create a temporary file to save the speech
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")    
    # Save the audio to the temporary filet
    tts.save(temp_audio.name)    
    # Close the temporary file to free up resources
    temp_audio.close()    
    # Send the temporary file as a response
    return send_file(temp_audio.name, as_attachment=True, download_name="speech.mp3")



#Duration - First 5 seconds and play audio
# with audio_file_ as source:
#   audio_file = recognizer.record(source, duration = 5.0)
#   result = recognizer.recognize_google(audio_data=audio_file)

#Offset - after 1 second and play audio
# with audio_file_ as source:
#   audio_file = recognizer.record(source, offset = 1.0)
#   result = recognizer.recognize_google(audio_data=audio_file)

#type(audio_file)

if __name__ == '__main__':
    app.run(debug=True)