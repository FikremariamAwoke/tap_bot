import asyncio
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)


async def start_node_script():
    # Start the Node.js script asynchronously
    process = await asyncio.create_subprocess_exec('node', 'ppptr.js', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return process


async def monitor_node_script(process):
    # Continuously read output from the Node.js script asynchronously
    try:
        while True:
            output = await process.stdout.readline()
            if output == '' and process.returncode is not None:
                break
            if output:
                logger.info(output.strip())
    except Exception as e:
        logger.error(f"[monitor_node_script] Error occurred: {e}")


async def main():
    # Start the Node.js script for the first time
    node_process = await start_node_script()

    # Run monitor_node_script asynchronously in a separate task
    asyncio.create_task(monitor_node_script(node_process))
    while True:
        try:
            # Check for new commits
            fetch_result = subprocess.run(['git', 'fetch'], check=True, capture_output=True, text=True)
            
            # Check if the local branch is behind the remote
            status_result = subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
            
            if "Your branch is behind" in status_result.stdout:
                print("New commit found. Pulling changes...")
                subprocess.run(['git', 'pull'], check=True)

                # Terminate the current Node.js process and start a new one
                logger.info("Restarting Node.js script due to new changes...")
                node_process.terminate()
                node_process = await start_node_script()

            else:
                print("No new commits found.")

        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        
        # Wait for 5 seconds
        time.sleep(10)

# Run the asynchronous tasks
asyncio.run(main())