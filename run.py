import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)

def start_node_script():
    # Start the Node.js script
    process = subprocess.Popen(['node', 'ppptr.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    monitor_node_script(process)
    return process

def monitor_node_script(process):
    # Continuously read output from the Node.js script
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logger.info(output.strip())
    except Exception as e:
       logger.error(f"Error occurred: {e}")

# Start the Node.js script for the first time
node_process = start_node_script()

while True:
    try:
        # Check for new commits
        fetch_result = subprocess.run(['git', 'fetch'], check=True, capture_output=True, text=True)
        
        # Check if the local branch is behind the remote
        status_result = subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
        
        if "Your branch is behind" in status_result.stdout:
            logger.info("New commit found. Pulling changes...")
            subprocess.run(['git', 'pull'], check=True)

            # Terminate the current Node.js process and start a new one
            logger.info("Restarting Node.js script due to new changes...")
            node_process.terminate()
            node_process = start_node_script()

        else:
            logger.info("No new commits found.")

    except Exception as e:
        logger.error(f"Error occurred: {e}")
    
    # Wait for 10 seconds before checking again
    time.sleep(10)
