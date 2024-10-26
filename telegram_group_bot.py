import time, json
from telegram import Update
import re
import urllib.parse
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from random import randrange
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)

# Regular expression pattern for extracting URLs
url_pattern = r'(https?://[^\s]+)'
replies = ["👌","👍","😜","😡","🤬","😒","😏","😒","🙂‍↔️","😞","🤗","🫡","🫡","🫡","🙌","👏","🫵","🦶","👀","🫷"]

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# Define the async function to respond with the names
async def active(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type in [update.message.chat.GROUP, update.message.chat.SUPERGROUP]:
        # Load the JSON file
        with open('links.json', 'r') as file:
            data = json.load(file)

        # Extract names from each link and format them for a single message
        names = [get_name_from_link(link["url"]) for link in data.get("links", [])]
        names = [name for name in names if name]  # Filter out None values

        # Send names in a single message
        if names:
            await update.message.reply_text(f"Here are all the active accounts:\n\n" + "\n".join(names))
        else:
            await update.message.reply_text("No valid names found in links.")
    else:
        await update.message.reply_text("I Don't know you 🤷‍♀️.")

def get_name_from_link(link):
    # Parse the URL and get the fragment part
    parsed_url = urllib.parse.urlparse(link)
    fragment = parsed_url.fragment
    
    # Parse the fragment into a dictionary of parameters
    params = urllib.parse.parse_qs(fragment)
    tg_web_app_data = params.get('tgWebAppData', [None])[0]
    
    if tg_web_app_data:
        # Decode and parse the user data
        decoded_data = urllib.parse.unquote(tg_web_app_data)
        user_match = re.search(r'user=([^&]*)', decoded_data)
        
        if user_match:
            user_json = urllib.parse.unquote(user_match.group(1))
            user = json.loads(user_json)
            
            # Get first and last name
            first_name = user.get("first_name", "")
            last_name = user.get("last_name", "")
            
            return f"{first_name} {last_name}"
    
    return None

# function to extract link
async def extract_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type in [update.message.chat.GROUP, update.message.chat.SUPERGROUP]:
        message = update.message.text  # Get the text from the message
        if message:
            links = re.findall(url_pattern, message)  # Find all links in the message
            if links:
                for link in links:
                    logger.info(f"\n\n--------------------------------------------------------------")
                    logger.info(f"Link found: {get_name_from_link(link)}")  # Print or log the links
                    response = add_link_to_json(link)
                    logger.info(f"--------------------------------------------------------------\n\n")
                    # Optionally, send the link back to the group or save it
                    await update.message.reply_text(response)
    else:
        message = update.message.text
        if message:
            links = re.findall(url_pattern, message)
            if links:
                for link in links:
                    logger.info(f"\n\n--------------------------------------------------------------")
                    logger.error(f"link {get_name_from_link(link)} is not from group")
                    logger.info(f"--------------------------------------------------------------\n\n")
        await update.message.reply_text("I Don't know you 🤷‍♀️.")

def add_link_to_json(new_url, json_file='links.json') -> str:
    # Get the current timestamp
    current_timestamp = int(time.time())
    # Define the threshold for 24 hours in seconds
    threshold = 24 * 60 * 60  # 24 hours in seconds
    
    # Check if the URL starts with the required prefix
    required_prefix = "https://tap1.urko.io/#tgWebAppData=query_id%"
    if not new_url.startswith(required_prefix):
        logger.error(f"Link does not start with '{required_prefix}' and will not be added.")
        return "❌Invalid Link❌"

    # Open and read the existing JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Remove links older than 24 hours
    data['links'] = [link for link in data['links'] if current_timestamp - link['addedAt'] < threshold]

    response = ""
    # Check for duplicates before adding the new link
    if not any(link['url'] == new_url for link in data['links']):
        # Append the new link
        data['links'].append({
            'url': new_url,
            'addedAt': current_timestamp
        })
        logger.info("Link added successfully.")
        response = f"{replies[randrange(len(replies) - 1)]}"
    else:
        logger.info("Duplicate link found; it will not be added.")
        response = "Link already exists 🙄.";
        return response

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty printing

    return response

app = ApplicationBuilder().token("7215862533:AAEzOQFD0K-zi2gW7Puw5xazq65eBnFzJ5c").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("active", active))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, extract_links))

app.run_polling()