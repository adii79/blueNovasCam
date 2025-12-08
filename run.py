# import subprocess

# print("Running main.py...")
# subprocess.run(["python", "esp.py"])

# print("Running firebase_update.py...")
# subprocess.run(["python", "fetch.py"])

# print("All scripts finished!")


import subprocess
import time

print("Starting esp.py...")
esp_process = subprocess.Popen(["python", "esp.py"])

print("Starting fetch.py...")
fetch_process = subprocess.Popen(["python", "fetch.py"])

print("Both scripts are running at the same time!")

# (Optional) wait for both to finish
esp_process.wait()
fetch_process.wait()

print("Both scripts finished!")