from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify
from flask_cors import CORS
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import vlc
import os
import webbrowser
import random
import platform
import pymongo
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)  # Enable CORS for your entire Flask app

# #Skils match
# # Connect to MongoDB
# mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# db = mongo_client['collaboration']

# # Retrieve data from MongoDB collections
# joblistings_collection = db['joblistings']
# profiles_collection = db['profiles']

# job_listings_data = list(joblistings_collection.find())
# freelancers_data = list(profiles_collection.find())

# #print("job_listings_data :", job_listings_data)

# # Create DataFrames from MongoDB data
# job_listings = pd.DataFrame(job_listings_data)
# freelancers = pd.DataFrame(freelancers_data)

# # Convert job listings and freelancer skills to text for skill matching
# job_skills_text = [' '.join(skills) for skills in job_listings['skills_required']]
# freelancer_skills_text = [' '.join(skills) for skills in freelancers['skills']]

# # Vectorize skills text using CountVectorizer
# vectorizer = CountVectorizer().fit(job_skills_text + freelancer_skills_text)
# job_skills_vectorized = vectorizer.transform(job_skills_text)
# freelancer_skills_vectorized = vectorizer.transform(freelancer_skills_text)

# # Compute cosine similarity between job listings and freelancer skills
# similarity_matrix = cosine_similarity(freelancer_skills_vectorized, job_skills_vectorized)

# # Create an empty list to store individual DataFrames
# matches_list = []

# # Iterate through each freelancer
# for i, freelancer_id in enumerate(freelancers['freelancer_id']):
#     # Find the job with the highest similarity score for the freelancer
#     best_match_index = similarity_matrix[i].argmax()
#     match_score = similarity_matrix[i, best_match_index]

#     # Create a DataFrame for the current match
#     match_df = pd.DataFrame({'freelancer_id': [freelancer_id], 'job_id': [job_listings['job_id'].iloc[best_match_index]], 'match_score': [match_score]})

#     # Append the DataFrame to the list
#     matches_list.append(match_df)

# # Concatenate all the individual DataFrames into one DataFrame
# matches = pd.concat(matches_list, ignore_index=True)

# # Sort matches by match_score in descending order
# matches = matches.sort_values(by='match_score', ascending=False)

# # Display the top matches
# print(matches)

# @app.route('/api/get-matches', methods=['GET'])
# def get_matches():
#     #print("Inside get_matches...!")
#     data_to_send = {"matches": matches.to_dict(orient='records')}  # Convert DataFrame to a list of dictionaries
#     #print("data_to_send: ", {"matches": matches.to_dict(orient='records')})
#     #print("matches.to_dict(orient='records') :", matches.to_dict(orient='records'))    
#     return jsonify({"matches": data_to_send})

#Chatting and VideoCall

def find_vlc_library():
    # List of possible locations where libvlc.dll might be found
    possible_paths = [
        r'C:\Program Files\VideoLAN\VLC\libvlc.dll'
    ]

    # Check each possible path
    for path in possible_paths:
        if os.path.exists(path):
            return path

    # If libvlc.dll is not found, return None
    return None

# Find the path to libvlc.dll
vlc_path = find_vlc_library()

# Initialize the VLC instance and player
if vlc_path:
    instance = vlc.Instance("--no-xlib", "--plugin-path={}".format(os.path.dirname(vlc_path)))
    player = instance.media_player_new()
else:
    messagebox.showerror("Error", "VLC library not found. Please make sure VLC is installed.")

# Define the choices and corresponding video URLs
choices = {
    "Spring Boot 3.0": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\pexels-nuray-20192905.mp4",
    "Salesforce Q&A": "https://www.youtube.com/watch?v=n3kUjExB1-0&list=PLaGX-30v1lh0ECrHwbN3C4hZJ8Msudreh",
    "canva": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\pexels_videos_2157006 (1080p).mp4",
    "earth1": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\video (2160p)(1).mp4",
    "earth2": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\video (2160p)(2).mp4",
    "earth3": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\video (2160p).mp4",
    "space": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\video (2160p)(3).mp4",
    "space1": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\video (2160p)(4).mp4",
    "aura": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\pexels-colin-jones-14909668 (720p).mp4", 
    "canva1": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\pexels-anna-tarazevich-6550969.mp4",
    "canva2": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_videos\\production_id 4151824 (2160p).mp4"
    # Add more choices and URLs as needed
}

# Function to play the video using vlc
def play_video(video_url):
    media = instance.media_new(video_url)
    player.set_media(media)
    if platform.system() == 'Windows':
        player.set_hwnd(video_frame.winfo_id())
    else:
        player.set_xwindow(video_frame.winfo_id())
    player.play()

# Function to play the selected video with VLC
def play_video_with_vlc():
    selected_choice = choice_var.get()
    video_url = choices.get(selected_choice)
    if video_url:
        play_video(video_url)
    else:
        messagebox.showerror("Error", "No video available for selected choice.")


# Function to handle chat prompts
def handle_prompt():
    prompt = prompt_entry.get().lower()
    responses = {
        "hello": ["Hello!", "Hi there!"],
        "how are you": ["I'm doing well, thank you!", "I'm fine, thanks for asking."],
        "name": ["My name is Chatbot.", "You can call me Chatbot."],
        "age": ["I'm just a computer program, so I don't have an age."],
        "salary": ["Your salary for this month is $5000."],
        "update": ["Please provide your updated personal information."],
        "leave": ["Please submit a leave request through the HR portal."],
        "feedback": ["Thank you for your feedback! Your opinion is valuable to us."],
        "ridhi": ["Hey, Riddhi, What are you doing during autumn break"],
        "basketball": ["How it is going on training..!"],
        "ncc": ["Hey Riddhi, Do not worry about NCC , campaign..You will have wonderful thing coming up on your way"],
        "9th class": ["I hope you are excited to go to next class..! I wish you have a wonderful futur ahead"],
        "lasya": ["Hi Lasya, Hello Medico, how is your preperation is going on, you got one more week for exam or back-log, enjoy"],
        "mbbs": ["Hi Lasya, Hello Doctor, I hope you will have wornderful future ahead..good luck"],
    }
    response = random.choice(responses.get(prompt, ["Sorry, I didn't understand that."]))
    chat_history_text.config(state=tk.NORMAL)
    chat_history_text.insert(tk.END, "You: ", "input_prompt")
    chat_history_text.insert(tk.END, f"{prompt}\n", "input_text")
    chat_history_text.insert(tk.END, "Chatbot: ", "response_prompt")
    chat_history_text.insert(tk.END, f"{response}\n\n", "response_text")
    chat_history_text.tag_config("input_prompt", foreground="blue")
    chat_history_text.tag_config("input_text", foreground="blue")
    chat_history_text.tag_config("response_prompt", foreground="green")
    chat_history_text.tag_config("response_text", foreground="green")
    chat_history_text.config(state=tk.DISABLED)
    chat_history_text.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Embedded VLC Player and Chatbot")

# Set the initial size of the window
root.geometry("400x600")

# Set window background color
root.configure(bg='lightgray')

# Create a frame for video player
video_frame = tk.Frame(root, bg='white')
video_frame.pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a Combobox to display the video options
choice_var = tk.StringVar(root)
choice_var.set("Select a video")  # Default choice

video_combobox = ttk.Combobox(root, textvariable=choice_var, values=list(choices.keys()))
video_combobox.pack(side=tk.TOP, padx=5, pady=5)

# Create a button to play the video using VLC
play_button = tk.Button(root, text="Play Video", command=play_video_with_vlc, width=10, bg='lightblue', relief=tk.GROOVE)
play_button.pack(side=tk.TOP, padx=5, pady=5)

# Create a frame for chat history and input
chat_frame = tk.Frame(root, bg='lightgray')
chat_frame.pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a text widget to display chat history
chat_history_text = tk.Text(chat_frame, wrap=tk.WORD, height=10)
chat_history_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a label and entry for user input prompt
prompt_label = tk.Label(chat_frame, text="Enter a prompt:", bg='lightgray')
prompt_label.pack(side=tk.LEFT, padx=5, pady=5)

prompt_entry = tk.Entry(chat_frame)
prompt_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to submit the prompt
submit_button = tk.Button(chat_frame, text="Submit", command=handle_prompt, bg='lightblue', relief=tk.GROOVE)
submit_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()


@app.route('/api/play-video', methods=['POST'])
def play_video():
    # Handle playing video functionality here
    play_video_with_vlc()
    # You can call your Python function to play the video
    return jsonify({'message': 'Video played successfully'})

@app.route('/api/chat', methods=['POST'])
def chat():
    # Handle chatbot interaction functionality here
    handle_prompt()
    # You can call your Python function to interact with the chatbot
    return jsonify({'message': 'Chatbot response'})




@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    #print('Received message:', message)
    emit('message', message, broadcast=True)

socketio.run(app, debug=True, port=5001)  # Change the port to 5001

if __name__ == '__main__':
    socketio.run(app, debug=True)
