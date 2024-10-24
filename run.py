import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)


async def start_node_script():
    # Start the Node.js script asynchronously
    process = await asyncio.create_subprocess_exec('node', 'ppptr.js', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, text=True)
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
        logger.error(f"Error occurred: {e}")


async def main():
    # Start the Node.js script for the first time
    node_process = await start_node_script()

    # Run monitor_node_script asynchronously in a separate task
    asyncio.create_task(monitor_node_script(node_process))

    while True:
        try:
            # Check for new commits
            fetch_result = await asyncio.create_subprocess_exec('git', 'fetch', check=True, capture_output=True, text=True)
            await fetch_result.wait()

            # Check if the local branch is behind the remote
            status_result = await asyncio.create_subprocess_exec('git', 'status', check=True, capture_output=True, text=True)
            await status_result.wait()

            if "Your branch is behind" in status_result.stdout:
                logger.info("New commit found. Pulling changes...")
                pull_result = await asyncio.create_subprocess_exec('git', 'pull', check=True, capture_output=True, text=True)
                await pull_result.wait()

                # Terminate the current Node.js process and start a new one
                logger.info("Restarting Node.js script due to new changes...")
                node_process.terminate()
                node_process = await start_node_script()

            else:
                logger.info("No new commits found.")

        except Exception as e:
            logger.error(f"Error occurred: {e}")

        # Wait for 10 seconds before checking again
        await asyncio.sleep(10)


# Run the asynchronous tasks
asyncio.run(main())