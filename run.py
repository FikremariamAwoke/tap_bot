import subprocess
import threading
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)

# Command to run in subprocess (e.g., infinite process like 'node ppptr.js')
command = ['node', 'ppptr.js']

# Function to print the subprocess logs
def log_subprocess_output(process):
    for line in process.stdout:
        logger.info(line.decode().strip() + "\n")

# Function to start the subprocess and log its output in a new thread
def start_process():
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log_thread = threading.Thread(target=log_subprocess_output, args=(process,), daemon=True)
    log_thread.start()
    return process, log_thread

# Initial start of the subprocess
process, log_thread = start_process()

# Create a custom event handler
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('links.json'):
            logger.info("links.json file changed. Restarting Node.js script...\n")

            global process, log_thread
            process.terminate()  # Terminate the current process
            process.wait()  # Wait for it to exit fully
            
            # Start a new process
            process, log_thread = start_process()

# Set up the watchdog observer
event_handler = ChangeHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)  # Monitor the current directory
observer.start()

try:
    while True:
        time.sleep(1)  # Keep the main thread alive
except KeyboardInterrupt:
    observer.stop()
except Exception as e:
    logger.error(f"[main][file-watcher] Error occurred: {e}\n")
finally:
    observer.join()
    if event_handler.process:
        event_handler.process.terminate()