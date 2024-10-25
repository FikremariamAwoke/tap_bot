import subprocess
import threading
import time
import logging

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

# Main loop to check for commits and restart the process if needed
while True:
    try:
        # Check for new commits
        fetch_result = subprocess.run(['git', 'fetch'], check=True, capture_output=True, text=True)
        
        # Check if the local branch is behind the remote
        status_result = subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
        
        if "Your branch is behind" in status_result.stdout:
            logger.info("New commit found. Pulling changes...\n")
            subprocess.run(['git', 'pull'], check=True)

            # Terminate the current Node.js process and start a new one
            logger.info("Restarting Node.js script due to new changes...\n")
            process.terminate()  # Terminate the process
            process.wait()  # Wait for it to exit fully

            # Start a new process and logging thread
            process, log_thread = start_process()

        else:
            logger.info("No new commits found.\n")

    except Exception as e:
        logger.error(f"[main][git-checker] Error occurred: {e}\n\n")
        
    # Wait for 10 seconds before the next check
    time.sleep(10)