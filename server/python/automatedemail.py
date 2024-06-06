import tkinter as tk
from datetime import datetime

# Function to open an HTML file with a mailto link
def open_mailto_link(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Work Event: {action} - {timestamp}"
    body = f"Hello,\n\nI just {action} at {timestamp}.\n\nBest regards,\nYour Name"

    # Create an HTML file with a mailto link
    mailto_link = f"mailto:raja.pinja@gmail.com?subject={subject}&body={body}"
    html_content = f'<a href="{mailto_link}">Click here to send the email</a>'
    
    with open("email.html", "w") as html_file:
        html_file.write(html_content)
    
    # Open the HTML file in the default web browser
    import webbrowser
    webbrowser.open("email.html")

# Create a GUI application
app = tk.Tk()
app.title("Work Actions")

# Define and configure buttons
buttons = [
    ("Signing In", "signing_in"),
    ("Going to Lunch", "going_to_lunch"),
    ("Back from Lunch", "back_from_lunch"),
    ("Stepping Away", "stepping_away")
]

for label, action in buttons:
    btn = tk.Button(app, text=label, command=lambda action=action: open_mailto_link(action))
    btn.pack()

# Start the GUI application
app.mainloop()
