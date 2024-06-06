import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import vlc
import os
import webbrowser
import random

# Function to find the path of libvlc.dll
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
    "Spring Boot 3.0": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\pexels-nuray-20192905.mp4",
    "Salesforce Q&A": "https://www.youtube.com/watch?v=n3kUjExB1-0&list=PLaGX-30v1lh0ECrHwbN3C4hZJ8Msudreh"
    # Add more choices and URLs as needed
}

# Function to play the video using vlc or web browser
def play_video(video_url):
    if video_url.startswith("http"):
        webbrowser.open_new(video_url)
    else:
        media = instance.media_new(video_url)
        player.set_media(media)
        player.play()

# Function to play the selected video with VLC or web browser
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
        "survey": ["Sure, I can help you with the survey. What is your feedback?"]
    }
    response = random.choice(responses.get(prompt, ["Sorry, I didn't understand that."]))
    chat_history_text.config(state=tk.NORMAL)
    chat_history_text.insert(tk.END, "You: ", "input_prompt")
    chat_history_text.insert(tk.END, f"{prompt}\n", "input_text")
    chat_history_text.insert(tk.END, "Chatbot: ", "response_prompt")
    chat_history_text.insert(tk.END, f"{response}\n\n", "response_text")
    chat_history_text.config(state=tk.DISABLED)
    chat_history_text.see(tk.END)

# Function to change window background color
def change_bg_color():
    color = color_var.get()
    root.config(bg=color)

# Create the main window
root = tk.Tk()
root.title("Video Player and Chatbot")

# Set the initial size of the window
root.geometry("800x600")

# Colors
window_colors = ["white", "light gray", "light blue", "light green", "light yellow", "light pink"]
text_colors = ["black", "dark gray", "dark blue", "dark green", "brown", "purple"]

# Create a frame for chat history and input
chat_frame = tk.Frame(root, bg=window_colors[0])
chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a text widget to display chat history
chat_history_text = tk.Text(chat_frame, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12), height=5)
chat_history_text.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar for the chat history
scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=chat_history_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history_text.config(yscrollcommand=scrollbar.set)

# Create a label and entry for user input
prompt_label = tk.Label(root, text="Enter a prompt:", bg=window_colors[0])
prompt_label.pack(padx=10, pady=5, side=tk.LEFT)

prompt_entry = tk.Entry(root, bg=window_colors[0])
prompt_entry.pack(padx=10, pady=5, side=tk.LEFT)

# Create a button to submit the prompt
submit_button = tk.Button(root, text="Submit", command=handle_prompt)
submit_button.pack(padx=10, pady=5, side=tk.LEFT)

# Create a Combobox to display the video options
choice_var = tk.StringVar(root)
choice_var.set("Select a video")  # Default choice

video_combobox = ttk.Combobox(root, textvariable=choice_var, values=list(choices.keys()))
video_combobox.pack(padx=10, pady=5, side=tk.LEFT)

# Create a button to play the video using VLC or web browser
play_button = tk.Button(root, text="Play Video", command=play_video_with_vlc)
play_button.pack(padx=10, pady=5, side=tk.LEFT)

# Create a label and Combobox to select window background color
color_label = tk.Label(root, text="Select window background color:")
color_label.pack(padx=10, pady=5, side=tk.LEFT)

color_var = tk.StringVar(root)
color_var.set(window_colors[0])  # Default color

color_combobox = ttk.Combobox(root, textvariable=color_var, values=window_colors, state="readonly")
color_combobox.pack(padx=10, pady=5, side=tk.LEFT)
color_combobox.bind("<<ComboboxSelected>>", lambda event: change_bg_color())

# Apply text colors and font styles
chat_history_text.tag_config("input_prompt", foreground=text_colors[0], font=("Arial", 12, "bold"))
chat_history_text.tag_config("input_text", foreground=text_colors[0], font=("Arial", 12))
chat_history_text.tag_config("response_prompt", foreground=text_colors[1], font=("Arial", 12, "bold"))
chat_history_text.tag_config("response_text", foreground=text_colors[1], font=("Arial", 12))

root.mainloop()
