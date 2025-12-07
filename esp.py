


# pip install opencv-python pillow requests numpy firebase-admin

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import requests
import numpy as np
import time

#some time the link changes figue it out to steam at fix url for local net
# ESP32 Camera Stream URL
# ESP32_URL = "http://192.168.173.230/capture"
# ESP32_CONFIG_URL = "http://192.168.92.230/control?var=framesize&val={}"
ESP32_URL = "http://10.169.230.254/capture"
ESP32_CONFIG_URL = "http://10.169.230.254/control?var=framesize&val={}"


# Firebase details
#use your firebase auth and host 

FIREBASE_HOST = "https://bluenova-7926f-default-rtdb.asia-southeast1.firebasedatabase.app/"
FIREBASE_AUTH = "hswIlGS4HikO4JnOF3spt8J3pe9rUwmHtDg53EBN"
FIREBASE_PATH = "/captured_images.json"

# Supported Resolutions for ESP32-CAM
RESOLUTIONS = {
    "QQVGA (160x120)": 0,
    "QVGA (320x240)": 1,
    "VGA (640x480)": 2,
    "SVGA (800x600)": 3,
    "XGA (1024x768)": 4,
    "SXGA (1280x1024)": 5,
    "UXGA (1600x1200)": 6
}

class ESP32StreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 Camera Stream")

        # Create a Label to show the video stream
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Resolution Selection Dropdown
        self.res_var = tk.StringVar(root)
        self.res_var.set("QVGA (320x240)")  # Default resolution

        self.res_dropdown = tk.OptionMenu(root, self.res_var, *RESOLUTIONS.keys(), command=self.change_resolution)
        self.res_dropdown.pack()

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack()

        # Start Video Streaming
        self.update_frame()
        
        # Capture and upload image every 10 seconds
        self.root.after(10000, self.capture_and_upload)

    def change_resolution(self, selected_res):
        """Change the resolution of the ESP32 camera."""
        res_value = RESOLUTIONS[selected_res]
        try:
            response = requests.get(ESP32_CONFIG_URL.format(res_value), timeout=1)
            if response.status_code == 200:
                print(f"Resolution changed to: {selected_res}")
            else:
                print(f"Failed to change resolution: {response.status_code}")
        except Exception as e:
            print(f"Error changing resolution: {e}")

    def update_frame(self):
        """Fetch and update the frame from ESP32."""
        try:
            response = requests.get(ESP32_URL, timeout=1)
            if response.status_code == 200:
                img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)

                    self.video_label.imgtk = imgtk
                    self.video_label.configure(image=imgtk)

        except Exception as e:
            print(f"Error fetching frame: {e}")

        # Refresh frame every 100 ms
        self.root.after(100, self.update_frame)

    def capture_and_upload(self):
        """Capture image from ESP32 and upload it to Firebase."""
        try:
            response = requests.get(ESP32_URL, timeout=1)
            if response.status_code == 200:
                img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if frame is not None:
                    # Convert frame to JPEG format
                    _, img_encoded = cv2.imencode(".jpg", frame)
                    img_bytes = img_encoded.tobytes()

                    # Convert image bytes to Base64 for Firebase
                    import base64
                    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

                    # Upload to Firebase
                    timestamp = int(time.time())
                    data = {
                        "timestamp": timestamp,
                        "image": img_base64
                    }

                    firebase_url = f"{FIREBASE_HOST}{FIREBASE_PATH}?auth={FIREBASE_AUTH}"
                    firebase_response = requests.post(firebase_url, json=data)

                    if firebase_response.status_code == 200:
                        print(f"Image uploaded to Firebase at {timestamp}")
                    else:
                        print(f"Failed to upload image: {firebase_response.status_code}")

        except Exception as e:
            print(f"Error capturing and uploading image: {e}")

        # Schedule next capture after 10 seconds
        self.root.after(10000, self.capture_and_upload)

# Run Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = ESP32StreamApp(root)
    root.mainloop()
