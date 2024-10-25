import time, json
from telegram import Update
import re
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from random import randrange

# Regular expression pattern for extracting URLs
url_pattern = r'(https?://[^\s]+)'
replies = ["👌","👍","😜","😡","🤬","😒","😏","😒","🙂‍↔️","😞","🤗","🫡","🫡","🫡","🙌","👏","🫵","🦶","👀","🫷"]

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# function to extract link
async def extract_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type in [update.message.chat.GROUP, update.message.chat.SUPERGROUP]:
        message = update.message.text  # Get the text from the message
        if message:
            links = re.findall(url_pattern, message)  # Find all links in the message
            if links:
                for link in links:
                    add_link_to_json(link)
                    print(f"Link found: {link}")  # Print or log the links
                    # Optionally, send the link back to the group or save it
                    await update.message.reply_text(f"{replies[randrange(len(replies) - 1)]}")
    else:
        print("not from group")

# Function to add a link to the JSON file
def add_link_to_json(new_url, json_file='links.json'):
    # Get the current timestamp
    current_timestamp = int(time.time())
    # Define the threshold for 24 hours in seconds
    threshold = 24 * 60 * 60  # 24 hours in seconds

    # Open and read the existing JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Remove links older than 24 hours
    data['links'] = [link for link in data['links'] if current_timestamp - link['addedAt'] < threshold]

    # Check for duplicates before adding the new link
    if not any(link['url'] == new_url for link in data['links']):
        # Append the new link
        data['links'].append({
            'url': new_url,
            'addedAt': current_timestamp
        })

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty printing

app = ApplicationBuilder().token("7215862533:AAEzOQFD0K-zi2gW7Puw5xazq65eBnFzJ5c").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, extract_links))

app.run_polling()