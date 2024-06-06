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

    # Automate opening Outlook and composing an email
    #os.system("start outlook.exe")
    #time.sleep(3)  # Wait for Outlook to open

    # Use the 'mailto' protocol to open the default email client (Outlook in this case)
    email_url = f'mailto:raja.pinja@outlook.com?subject={subject}&body={body}'
    os.system(f'start {email_url}')

    # Automate typing email details
    pyautogui.typewrite("raja.pinja@outlook.com")  # Replace with the recipient's email
    pyautogui.press("tab")
    pyautogui.typewrite(subject)
    pyautogui.press("tab")
    pyautogui.typewrite(body)

    # Send the email
    pyautogui.hotkey("ctrl", "enter")

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

