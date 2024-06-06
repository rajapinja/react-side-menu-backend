import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import vlc
import os

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
    "Spring Boot 3.0": "https://www.youtube.com/watch?v=hUfqT8gVX7c&list=PLsQ8yXXZeOzA4TYQYBnX8XwYXzV2iSnrh",
    "Salesforce Q&A": "https://www.youtube.com/watch?v=n3kUjExB1-0&list=PLaGX-30v1lh0ECrHwbN3C4hZJ8Msudreh"
    # Add more choices and URLs as needed
}

# Function to play the selected video using vlc
def vlc_video(video_url):
    media = instance.media_new(video_url)
    player.set_media(media)
    player.play()

# Function to play the selected video
def play_video():
    selected_choice = choice_var.get()
    video_url = choices.get(selected_choice)
    if video_url:
        vlc_video(video_url)
    else:
        messagebox.showerror("Error", "No video available for selected choice.")

# Create the main window
root = tk.Tk()
root.title("Video Player")

# Create a variable to store the selected choice
choice_var = tk.StringVar(root)
choice_var.set("Select a video")  # Default choice

# Create a Combobox to display the video options
video_combobox = ttk.Combobox(root, textvariable=choice_var, values=list(choices.keys()))
video_combobox.pack(padx=10, pady=5)

# Create a button to play the video within the Tkinter window
play_button = tk.Button(root, text="Play Video", command=play_video)
play_button.pack(padx=10, pady=5)

root.mainloop()
