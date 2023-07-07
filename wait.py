import os
import time
import subprocess

file_path = '/path/to/file.txt'
drone_file = '/path/to/drone1.py'

while not os.path.exists(file_path):
    print(f"File '{file_path}' not found. Waiting...")
    time.sleep(1)  # Wait for 1 second before checking again

print(f"File '{file_path}' found! Triggering 'drone1.py'...")
subprocess.run(['python', drone_file])  # Trigger 'drone1.py'
