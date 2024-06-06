import os
import time
import pyautogui
import datetime

# Function to send an email with a timestamp
def send_email(action):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Work Event: {action} - {timestamp}"
    body = f"Hello,\n\nI just {action} at {timestamp}.\n\nBest regards,\nYour Name"

    # Use the 'mailto' protocol to open the default email client (Outlook in this case)
    email_url = f'mailto:raja_pinja@yahoo.com?subject={subject}&body={body}'
    os.system(f'start {email_url}')

# Create interactive buttons on the desktop
desktop_button_positions = {
    "Signing In": (100, 100),
    "Going to Lunch": (100, 150),
    "Back from Lunch": (100, 200),
    "Stepping Away": (100, 250)
}

# Main loop
while True:
    print("Available actions:")
    for action in desktop_button_positions.keys():
        print(f"- {action}")
    user_input = input("Enter the action you want to perform: ")

    if user_input in desktop_button_positions:
        action = user_input
        x, y = desktop_button_positions[action]
        pyautogui.click(x, y)
        send_email(action)
        print(f"Email sent for {action}.")
    else:
        print("Invalid action. Please choose from the available actions.")
