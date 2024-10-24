import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to the Node.js script
node_script = "ppptr.js"

# Define a handler to restart the Node.js process
class NodeRestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(node_script):
            print(f"{node_script} has changed. Restarting Node.js process...")
            self.restart_node_process()

    def restart_node_process(self):
        global node_process
        if node_process:
            node_process.terminate()  # Terminate the existing process
            node_process.wait()  # Wait for it to terminate
        # Start a new Node.js process
        global node_process
        node_process = subprocess.Popen(['node', node_script])

# Initialize the Node.js process
node_process = subprocess.Popen(['node', node_script])

# Watch for changes in the current directory
event_handler = NodeRestartHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)

# Start observing
observer.start()
print("Watching for changes in ppptr.js...")

# Get the current directory
git_folder = os.getcwd()

while True:
    try:
        # Check for new commits
        fetch_result = subprocess.run(['git', 'fetch'], check=True, capture_output=True, text=True)
        
        # Check if the local branch is behind the remote
        status_result = subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
        
        if "Your branch is behind" in status_result.stdout:
            print("New commit found. Pulling changes...")
            subprocess.run(['git', 'pull'], check=True)
            # Optionally restart the Node.js process if the pull affects ppptr.js
            print(f"{node_script} has changed after pulling. Restarting Node.js process...")
            node_process.terminate()  # Terminate the existing process
            node_process.wait()  # Wait for it to terminate
            node_process = subprocess.Popen(['node', node_script])  # Restart the process
        else:
            print("No new commits found.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    
    # Wait for 5 seconds
    time.sleep(5)

# Clean up on exit
observer.stop()
node_process.terminate()
node_process.wait()
observer.join()
