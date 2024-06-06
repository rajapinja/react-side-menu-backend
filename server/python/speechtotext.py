# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import ffmpeg
import os
from google.cloud import speech
import subprocess
from werkzeug.utils import secure_filename  # Import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for your entire Flask app

recognizer = sr.Recognizer()


# Check if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    print("ERROR: The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
else:
    print("GOOGLE_APPLICATION_CREDENTIALS is set to:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])


# Set the project ID
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

# Create a client instance of the Google Cloud Speech-to-Text API
client = speech.SpeechClient()

# Load the Google Web Speech API key JSON file
key_path = "\server\python\_Google_Key\fair-yew-122918-512856ecb9bc.json"
#credentials = sr.ServiceCredentials.from_service_account_file(key_path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# def convert_audio_to_wav(audio_file_path):
#     # Load the audio file and convert it to WAV format
#     input_audio = ffmpeg.input(audio_file_path)
#     wav_path = os.path.splitext(audio_file_path)[0] + ".wav"
#     output_audio = ffmpeg.output(input_audio, wav_path)
#     ffmpeg.run(output_audio, overwrite_output=True)
#     return wav_path

# def convert_audio_to_wav(audio_file):
#     if not audio_file:
#         return None

#     # Extract the file name from the FileStorage object
#     audio_file_name = audio_file.filename

#     # Create a unique file name for the WAV file
#     wav_file_name = os.path.splitext(audio_file_name)[0] + ".wav"
    
#     # Save the audio file to the "uploads" directory
#     audio_file_path = os.path.join('uploads', audio_file_name)
#     audio_file.save(audio_file_path)

#     # Convert the saved audio file to WAV format
#     wav_path = os.path.join('uploads', wav_file_name)
#     input_audio = ffmpeg.input(audio_file_path, executable='C:\\_Softwares\\ffmpeg\\bin\\ffmpeg.exe')
#     output_audio = ffmpeg.output(input_audio, wav_path, executable='C:\\_Softwares\\ffmpeg\\bin\\ffmpeg.exe')
#     ffmpeg.run(output_audio, overwrite_output=True)

#     return wav_path


# def convert_audio_to_wav(audio_file):
#     # Define the path to ffmpeg.exe
#     ffmpeg_path = r'C:\_Softwares\ffmpeg\bin\ffmpeg.exe'

#     # Generate a secure filename for the audio file
#     audio_filename = secure_filename(audio_file.filename)
    
#     # Save the uploaded audio file temporarily
#     temp_audio_path = f'temp/{audio_filename}'  # Use an appropriate temporary directory

#     audio_file.save(temp_audio_path)

#     # Construct the command to convert the audio to WAV
#     cmd = [
#         ffmpeg_path,
#         '-i', temp_audio_path,
#         '-f', 'wav',
#         '-y',  # Overwrite output if it exists
#         temp_audio_path + '.wav'  # Output file path
#     ]

#     try:
#         subprocess.run(cmd, check=True)
#         return temp_audio_path + '.wav'
#     except subprocess.CalledProcessError as e:
#         print("Error running ffmpeg:", e)
#         return None

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

# @app.route('/api/speech-to-text', methods=['POST'])
# def speech_to_text_api():
#     if 'audio' not in request.files:
#         return jsonify({'error': 'No audio file provided'})

#     audio_file = request.files['audio']

#     # Ensure that the uploaded file has a valid name
#     if not audio_file.filename:
#         return jsonify({'error': 'Invalid audio file name'})

#     audio_file_path = os.path.join('temp', secure_filename(audio_file.filename))

#     # If the file is not in WAV format, convert it to WAV
#     if not is_wav_file(audio_file_path):
#         audio_file_path = convert_audio_to_wav(audio_file)

   
#     if audio_file_path:
#         with sr.AudioFile(audio_file_path) as source:
#             audio = recognizer.record(source)
#     else:
#         return jsonify({'error': 'Failed to convert audio to WAV'})

#     try:
#        # Configure the recognizer with the credentials
#         text = recognizer.recognize_google_cloud(audio)
#         print("text :", text)
#         return jsonify({'text': text})  # Return recognized text
#     except sr.UnknownValueError:
#         return jsonify({'error': 'Could not understand audio'})
#     except sr.RequestError as e:
#         return jsonify({'error': f'Error with the speech recognition service: {str(e)}'})


@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text_api():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']

    # Ensure that the uploaded file has a valid name
    if not audio_file.filename:
        return jsonify({'error': 'Invalid audio file name'})

    audio_file_path = os.path.join('temp', secure_filename(audio_file.filename))

    # If the file is not in WAV format, convert it to WAV
    if not is_wav_file(audio_file_path):
        audio_file_path = convert_audio_to_wav(audio_file)

    # Use the client to perform recognition
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    # Perform recognition
    response = client.recognize(audio=audio, config=config)

    # Extract recognized text from the response
    text = ""
    for result in response.results:
        text += result.alternatives[0].transcript

    return jsonify({'text': text})


if __name__ == '__main__':
    app.run(debug=True)



# def is_wav_file(file_path):
#     return os.path.splitext(file_path)[1].lower() == '.wav'

# @app.route('/api/speech-to-text', methods=['POST'])
# def speech_to_text_api():
#     audio_file = request.files['audio']
#     audio_file_path = os.path.join('uploads', audio_file.filename)

#     # If the file is not in WAV format, convert it to WAV
#     if not is_wav_file(audio_file_path):
#         audio_file_path = convert_audio_to_wav(audio_file)

#     if audio_file_path:
#         with sr.AudioFile(audio_file_path) as source:
#             audio = recognizer.record(source)
#     else:
#         with sr.Microphone() as source:
#             print("Speak something...")
#             audio = recognizer.listen(source)
    
#     try:
#         text = recognizer.recognize_google(audio)
#         return jsonify({'text': text})
#     except sr.UnknownValueError:
#         return jsonify({'error': 'Could not understand audio'})
#     except sr.RequestError as e:
#         return jsonify({'error': f'Error with the speech recognition service: {str(e)}'})



#To Future Use only -- Below Code
  
#The simplest way to check the type of an audio file is by examining its file extension. 
#Common audio file extensions include .wav, .mp3, .ogg, .flac, .aac, and more. 
#You can use the os.path.splitext() function to extract the file extension from the file path and then compare it to known audio file extensions.

def get_audio_file_type(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.aac']:
        audio = ffmpeg.from_mp3('your_audio.mp3')
        return audio.export('output_audio.wav', format='wav')
    else:
        return 'Unknown Audio'

file_path = 'your_audio.mp3'  # Replace with your audio file path
audio_type = get_audio_file_type(file_path)
print(f'Type of audio file: {audio_type}')


#Examine the header information of the audio file. Different audio formats have specific headers that contain information about the file format. 
#You can use specialized libraries like audioread to inspect the header and determine the file type.
def get_audio_file_type(file_path):
    try:
        with audioread.audio_open(file_path) as f:
            audio_format = f.format
            return audio_format
    except Exception as e:
        return 'Unknown'

file_path = 'your_audio.mp3'  # Replace with your audio file path
audio_type = get_audio_file_type(file_path)
print(f'Audio file format: {audio_type}')



if __name__ == '__main__':
    app.run(debug=True)
