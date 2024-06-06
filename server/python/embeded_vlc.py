import tkinter as tk
from tkinter import ttk
import vlc
import time
import platform

# Create a Tkinter window
root = tk.Tk()
root.title("Embedded VLC Player")
root.geometry("800x600")

# Create a frame for VLC player
vlc_frame = ttk.Frame(root)
vlc_frame.pack(fill=tk.BOTH, expand=True)

# Initialize VLC instance
instance = vlc.Instance('--no-xlib')

# Create VLC player
player = instance.media_player_new()

# Set up media
media = instance.media_new('C:\\Users\\raja_\\OneDrive\\Desktop\\_QuickStart\\_ELK_Logging\\pexels-nuray-20192905.mp4')
player.set_media(media)

# Create a VLC widget
vlc_widget = ttk.Frame(vlc_frame)
vlc_widget.pack(fill=tk.BOTH, expand=True)

# Embed the VLC player into the Tkinter window
if platform.system() == 'Windows':
    player.set_hwnd(vlc_widget.winfo_id())
else:
    player.set_xwindow(vlc_widget.winfo_id())

# Play the media
player.play()

# Function to stop the media
def stop_media():
    player.stop()

# Create a stop button
stop_button = ttk.Button(root, text="Stop", command=stop_media)
stop_button.pack(pady=10)

root.mainloop()
