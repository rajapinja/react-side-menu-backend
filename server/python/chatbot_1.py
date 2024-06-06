import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import vlc
import os
import webbrowser
import random
import platform

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
    "Salesforce Q&A": "https://www.youtube.com/watch?v=n3kUjExB1-0&list=PLaGX-30v1lh0ECrHwbN3C4hZJ8Msudreh",
     "canva": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\pexels_videos_2157006 (1080p).mp4",
      "earth1": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\video (2160p)(1).mp4",
       "earth2": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\video (2160p)(2).mp4",
        "space": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\video (2160p)(3).mp4",
         "space1": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\video (2160p)(4).mp4",
         "aura": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\pexels-colin-jones-14909668 (720p).mp4",
         "space3": "C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\video (2160p).mp4",

    # Add more choices and URLs as needed
}

# Function to play the video using vlc or web browser
def play_video(video_url):
    if video_url.startswith("http"):
        webbrowser.open_new(video_url)
    else:
        media = instance.media_new(video_url)
        player.set_media(media)
        if platform.system() == 'Windows':
            player.set_hwnd(video_frame.winfo_id())
        else:
            player.set_xwindow(video_frame.winfo_id())
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
    chat_history_text.tag_config("input_prompt", foreground="blue")
    chat_history_text.tag_config("input_text", foreground="blue")
    chat_history_text.tag_config("response_prompt", foreground="green")
    chat_history_text.tag_config("response_text", foreground="green")
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

# Create a frame for video player
video_frame = tk.Frame(root, bg=window_colors[0])
video_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a Combobox to display the video options
choice_var = tk.StringVar(root)
choice_var.set("Select a video")  # Default choice

video_combobox = ttk.Combobox(video_frame, textvariable=choice_var, values=list(choices.keys()))
video_combobox.pack(padx=5, pady=5, side=tk.LEFT)

# Create a button to play the video using VLC or web browser
play_button = tk.Button(video_frame, text="Play Video", command=play_video_with_vlc)
play_button.pack(padx=5, pady=5, side=tk.LEFT)

# Create a frame for chat history and input
chat_frame = tk.Frame(root, bg=window_colors[0])
chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create a text widget to display chat history
chat_history_text = tk.Text(chat_frame, wrap=tk.WORD, bg="white", fg="blue", font=("Consolas", 12), height=5)
chat_history_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a scrollbar for the chat history
scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=chat_history_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history_text.config(yscrollcommand=scrollbar.set)

# Create a frame for prompt and window color selection
options_frame = tk.Frame(root, bg=window_colors[0])
options_frame.pack(padx=10, pady=5, fill=tk.X, side=tk.BOTTOM)

# Create a label and entry for user input prompt
prompt_label = tk.Label(options_frame, text="Enter a prompt:", bg=window_colors[0])
prompt_label.grid(row=0, column=0, padx=5, pady=5)

prompt_entry = tk.Entry(options_frame, bg=window_colors[0], width=50)
prompt_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a button to submit the prompt
submit_button = tk.Button(options_frame, text="Submit", command=handle_prompt)
submit_button.grid(row=0, column=2, padx=5, pady=5)

# Create a label and Combobox to select window background color
color_label = tk.Label(options_frame, text="Select window background color:")
color_label.grid(row=1, column=0, padx=5, pady=5)

color_var = tk.StringVar(root)
color_var.set(window_colors[0])  # Default color

color_combobox = ttk.Combobox(options_frame, textvariable=color_var, values=window_colors, state="readonly")
color_combobox.grid(row=1, column=1, padx=5, pady=5)
color_combobox.bind("<<ComboboxSelected>>", lambda event: change_bg_color())

root.mainloop()
