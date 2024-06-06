import tkinter as tk
from tkinter import scrolledtext, colorchooser
from nltk.chat.util import Chat, reflections
import json
import random  # For selecting random responses

# Function to read patterns and responses from a JSON file
def read_patterns_from_json(file_path):
    with open(file_path, 'r') as file:
        patterns_data = json.load(file)
    return patterns_data['patterns']

# Initialize chatbot patterns and responses
patterns = read_patterns_from_json('patterns.json')

# Function to send message and get response
def send_message():
    user_input = input_entry.get().lower()  # Convert input to lowercase for case-insensitive matching
    response = None  # Initialize response variable
    
    # Check if input matches any pattern and select a random response
    for pattern_data in patterns:
        if pattern_data["pattern"] in user_input:
            responses = pattern_data["responses"]
            response = random.choice(responses)
            break
    
    if response is None:
        response = "I'm sorry, I didn't understand that. Could you please rephrase?"

    display_message("You: " + user_input, "blue")  # Display user message in blue color
    display_message("Chatbot: " + response, "green")  # Display chatbot message in green color
    input_entry.delete(0, tk.END)

# Function to display messages with specified color
def display_message(message, color):
    response_text.config(state=tk.NORMAL)
    response_text.insert(tk.END, message + "\n", color)
    response_text.config(state=tk.DISABLED)

# Function to change window color
def change_window_color():
    color = colorchooser.askcolor(title="Choose a color")[1]  # Get the selected color
    popup_window.configure(bg=color)  # Set the background color of the window

# Create pop-up window
popup_window = tk.Tk()
popup_window.title("Employee Chatbot")

# Create input entry
input_entry = tk.Entry(popup_window, width=50)
input_entry.pack(padx=10, pady=10)

# Create response text area
response_text = scrolledtext.ScrolledText(popup_window, width=60, height=20)
response_text.pack(padx=10, pady=10)

# Create send button
send_button = tk.Button(popup_window, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

# Create color picker button
color_button = tk.Button(popup_window, text="Change Window Color", command=change_window_color)
color_button.pack(padx=10, pady=10)

# Configure tag for different text colors
response_text.tag_config("blue", foreground="blue")   # User messages in blue
response_text.tag_config("green", foreground="green") # Chatbot messages in green

popup_window.mainloop()
