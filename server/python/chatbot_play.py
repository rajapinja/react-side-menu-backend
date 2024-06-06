import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinter import messagebox

# Define the choices and corresponding video URLs
choices = {
    "Spring Boot 3.0": "https://www.youtube.com/watch?v=hUfqT8gVX7c&list=PLsQ8yXXZeOzA4TYQYBnX8XwYXzV2iSnrh",
    "Salesforce Q&A": "https://www.youtube.com/watch?v=n3kUjExB1-0&list=PLaGX-30v1lh0ECrHwbN3C4hZJ8Msudreh"
    # Add more choices and URLs as needed
}

# Function to play the video in a web browser
def play_video_browser():
    selected_choice = choice_var.get()
    video_url = choices.get(selected_choice)
    if video_url:
        webbrowser.open_new(video_url)
    else:
        messagebox.showerror("Error", "No video available for selected choice.")

# Function to display the pop-up window with video playback
def show_popup():
    selected_choice = choice_var.get()
    video_url = choices.get(selected_choice)
    if video_url:
        popup_window = tk.Toplevel(root)
        popup_window.title("Video Player")

        # Open the video URL in the default web browser
        webbrowser.open_new(video_url)
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

# Create a button to play the video in the default web browser
browser_button = tk.Button(root, text="Play Video in Browser", command=play_video_browser)
browser_button.pack(padx=10, pady=5)

# Create a button to show the pop-up window with video playback
popup_button = tk.Button(root, text="Play Video in Popup", command=show_popup)
popup_button.pack(padx=10, pady=5)

root.mainloop()

