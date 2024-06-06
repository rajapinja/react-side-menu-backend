import tkinter as tk
from datetime import datetime
import win32com.client
import os

def send_email_outlook_desktop(action):
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)  # 0 represents the index for creating a new mail item

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Work Event: {action} - {timestamp}"
    body = f"Hello,\n\nI just {action} at {timestamp}.\n\nBest regards,\nRaja Pinja"

    mail.Subject = subject
    mail.Body = body
    mail.To = "raja.pijnja@gmail.com"  # Replace with the recipient's email address
    mail.Send()

def send_email_outlook_app(action):
    # Command to open the Outlook app
    os.system("start outlook:")

    # Pause briefly to allow Outlook to open
    import time
    time.sleep(5)

    # Create an HTML file with a mailto link
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Work Event: {action} - {timestamp}"
    body = f"Hello,\n\nI just {action} at {timestamp}.\n\nBest regards,\nRaja Pinja"

    # Create the HTML content with a mailto link
    mailto_link = f"mailto:raja.pinja@gmail.com?subject={subject}&body={body}"
    html_content = f'<a href="{mailto_link}">Click here to send the email</a>'

    with open("email.html", "w") as html_file:
        html_file.write(html_content)

    # Open the HTML file in the default web browser
    import webbrowser
    webbrowser.open("email.html")

def send_email(action, client_choice, status_label):
    if client_choice == "Outlook Desktop":
        try:
            send_email_outlook_desktop(action)
            status_label.config(text=f"Email sent for {action} via Outlook Desktop.")
        except:
            status_label.config(text="Outlook Desktop not found. Email not sent.")
    elif client_choice == "Outlook App":
        send_email_outlook_app(action)
        status_label.config(text=f"Email sent for {action} via Outlook App.")

def on_button_click(action, client_choice, status_label):
    send_email(action, client_choice, status_label)

app = tk.Tk()
app.title("Work Email Automation")

# Define and configure buttons
buttons = [
    ("Signing In", "signing_in"),
    ("Going to Lunch", "going_to_lunch"),
    ("Back from Lunch", "back_from_lunch"),
    ("Stepping Away", "stepping_away")
]

status_label = tk.Label(app, text="", fg="green")
status_label.pack()

for label, action in buttons:
    for client in ["Outlook Desktop", "Outlook App"]:
        btn = tk.Button(app, text=f"Send via {client}", command=lambda action=action, client=client: on_button_click(action, client, status_label))
        btn.pack()

app.mainloop()
