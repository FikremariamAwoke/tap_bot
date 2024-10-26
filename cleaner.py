import time, json
import re
import urllib.parse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Use the logger
logger = logging.getLogger(__name__)

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

def get_user_id_from_link(link):
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
            
            # Get user id            
            return f"{user['id']}"
    
    return None

def timestamp_to_readable(timestamp):
    import datetime

    # Convert to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    # Format the datetime object as a string
    readable_format = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return readable_format

def remove_duplicate(json_file='links.json') -> str:
    current_timestamp = int(time.time())
    threshold = 24 * 60 * 60  # 24 hours in seconds

    # Open and read the existing JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    size_of_links = len(data['links'])
    
    print("--------------------------------------Existing---------------------------------------------")
    for link in data['links']:
        print(f"{get_name_from_link(link['url'])} | {get_user_id_from_link(link['url'])} | {timestamp_to_readable(link['addedAt'])}")
        # TODO: remove duplicate from list by its id. keep the latest one using the added at
    print("------------------------------------------------------------------------------------------")

    # Keep track of the latest links by user ID
    latest_links = {}

    for link in data['links']:
        if current_timestamp - link['addedAt'] < threshold:
            user_id = get_user_id_from_link(link['url'])
            if user_id:
                # If the user ID is already in latest_links, compare timestamps
                if user_id not in latest_links or link['addedAt'] > latest_links[user_id]['addedAt']:
                    latest_links[user_id] = link

    # Convert the latest_links dictionary back to a list
    data['links'] = list(latest_links.values())

    size_of_updated_links = len(data['links'])

    print("--------------------------------------Cleaned---------------------------------------------")
    for link in data['links']:
       print(f"{get_name_from_link(link['url'])} | {get_user_id_from_link(link['url'])} | {timestamp_to_readable(link['addedAt'])}")
    print("------------------------------------------------------------------------------------------")

    if size_of_links != size_of_updated_links:
        # Write the updated data back to the JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)  # Use indent for pretty printing
        logger.info("Removed duplicates and updated the JSON file.\n\n\n")


try:
    while True:
        remove_duplicate()
        time.sleep(10)
except Exception as e:
    logger.error(f"[cleaner]: {e}")