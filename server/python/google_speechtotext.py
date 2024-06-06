import io
import os



from google.cloud import speech

# Set the project ID
PROJECT_ID = os.environ.get("fair-yew-122918se")

# Create a Speech client
client = speech.SpeechClient()

# Set the audio file path
audio_file_path = "C:\_Raja\_React_Projects\remoteworker_collaboration_platform\server\python\temp\celtic-irish-scottish-tin-whistle-background-music-10455.wav"

# Read the audio file
with io.open(audio_file_path, "rb") as audio_file:
    content = audio_file.read()

# Construct the request
config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)

audio = speech.types.RecognitionAudio(content=content)

response = client.recognize(config=config, audio=audio)

# Print the results
for result in response.results:
    print(result.alternatives[0].transcript)
