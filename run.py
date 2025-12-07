import subprocess

print("Running main.py...")
subprocess.run(["python", "esp.py"])

print("Running firebase_update.py...")
subprocess.run(["python", "fetch.py"])

print("All scripts finished!")
