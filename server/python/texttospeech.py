from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data['text']
    tts = gTTS(text)
    output_path = 'output_1.mp3'
    tts.save(output_path)
    return jsonify({'message': 'Speech generated', 'audio_url': f'/get-audio/{output_path}'})

@app.route('/get-audio/<path:filename>')
def get_audio(filename):
    return send_from_directory('', filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
