import tkinter as tk
from tkinter import scrolledtext, colorchooser
from nltk.chat.util import Chat, reflections

# Define conversation patterns and responses
patterns = [
    (r'(.*)salary(.*)', ['Your salary for this month is $5000.']),
    (r'(.*)update(.*)', ['Please provide your updated personal information.']),
    (r'(.*)leave(.*)', ['Please submit a leave request through the HR portal.']),
    (r'(.*)feedback(.*)', ['Thank you for your feedback! Your opinion is valuable to us.']),
    (r'(.*)survey(.*)', ['Sure, I can help you with the survey. What is your feedback?']),
    (r'(.*)', ["I'm sorry, I didn't understand that. Could you please rephrase?"])
]

# Create chatbot
chatbot = Chat(patterns, reflections)

# Function to send message and get response
def send_message():
    user_input = input_entry.get()
    response = chatbot.respond(user_input)
    display_message("You: " + user_input, "blue")  # Display user message in blue color
    
    # Check if the response is a list
    if isinstance(response, list):
        # Concatenate all responses into a single string
        response = ' '.join(response)
    
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
