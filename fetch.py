
import tkinter as tk
from PIL import Image, ImageTk
import requests
import base64
import io

# Firebase details
#use your firebase auth and host 
# https://bluenova-7926f-default-rtdb.asia-southeast1.firebasedatabase.app/
FIREBASE_HOST = "https://bluenova-7926f-default-rtdb.asia-southeast1.firebasedatabase.app/"
FIREBASE_AUTH = "hswIlGS4HikO4JnOF3spt8J3pe9rUwmHtDg53EBN"
FIREBASE_PATH = "/captured_images.json"  # Firebase path for images

class FirebaseImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Latest Image Viewer")

        # Create label to display image
        self.image_label = tk.Label(root, text="Fetching image...", font=("Arial", 14))
        self.image_label.pack()

        # Start fetching images
        self.update_image()

    def fetch_latest_image(self):
        """Fetch the latest image from Firebase."""
        try:
            firebase_url = f"{FIREBASE_HOST}{FIREBASE_PATH}?auth={FIREBASE_AUTH}"
            response = requests.get(firebase_url)

            if response.status_code == 200 and response.json():
                images = response.json()
                latest_entry = max(images.values(), key=lambda x: x["timestamp"])
                return latest_entry["image"]

        except Exception as e:
            print(f"Error fetching image from Firebase: {e}")

        return None

    def update_image(self):
        """Update the displayed image with the latest one from Firebase."""
        image_data = self.fetch_latest_image()
        if image_data:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image = image.resize((400, 300), Image.LANCZOS)  # Resize for display

            imgtk = ImageTk.PhotoImage(image)
            self.image_label.config(image=imgtk)
            self.image_label.image = imgtk  # Keep a reference to prevent garbage collection

        self.root.after(10000, self.update_image)  # Auto-update every 10 seconds

# Run Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = FirebaseImageViewer(root)
    root.mainloop()
