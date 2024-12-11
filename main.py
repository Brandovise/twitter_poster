import time
from ChatGPTCleint import ChatGPTClient
from twitter_class import TwitterPoster
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter credentials loaded from environment variables
x_client_id = os.getenv("TWITTER_CLIENT_ID")
x_client_secret = os.getenv("TWITTER_CLIENT_SECRET")
x_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
x_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
x_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
x_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
x_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Google Sheets information loaded from environment variables
google_sheet_id = os.getenv("GOOGLE_SHEET_ID")
range_name = os.getenv("GOOGLE_SHEET_RANGE")

# CHATGPT API
chatgpt_API = os.getenv("CHATGPT_API")

# Initialize the SocialMediaPoster class
poster = TwitterPoster()

# Initialize the ChatGPT Client instance
client = ChatGPTClient(chatgpt_API)
receipe_folder = "recipe"
post_folder = "post"
client.set_recipe_post_folder(receipe_folder, post_folder)

# Fetch data from Google Sheet
client.get_excel_values(google_sheet_id, range_name)

# Authenticate Twitter client
poster.authenticate(
    x_client_id, x_client_secret, x_consumer_key, x_consumer_secret, 
    x_access_token, x_access_token_secret, x_bearer_token
)

# Social media platforms to post on
post_in = ['twitter']
post_in_boolean = [1]

# Process each row from the data fetched from the Google Sheet
for row_number in range(len(client.exda.data)):
    temp_date = client.exda.data[row_number]['Date']
    input_date = datetime.strptime(temp_date, '%m/%d/%Y')
    today_date = datetime.now().date()

    if input_date.date() == today_date:
        try:
            # Prepare post data (title and link)
            poster.title = client.exda.data[row_number]['Title']
            poster.url_in = client.exda.data[row_number]['Link']

            # Define paths for images and text files
            folder_path = f"{post_folder}/{client.exda.data[row_number]['Day']}"
            imagepath = f"{folder_path}/image.png"
            imagepath_txt = f"{folder_path}/image.txt"
            client.get_image(row_number)
            print(f"Image has been received for {client.exda.data[row_number]['Day']}")

        except Exception as e:
            print(f"An error occurred while preparing post data: {e}")



        if post_in_boolean[0]:
            try:
                # Generate Twitter post content
                post_type = "twitter"
                client.get_social_media_post(row_number, post_type)
                print(f"Twitter Post created for {client.exda.data[row_number]['Day']}")
            except Exception as e:
                print(f"Error in generating Twitter post: {e}")

            try:
                # Read Twitter message content from file
                tweet_message_path = f"{folder_path}/{post_type}_post.txt"
                tweet_message = client.read_text_file(tweet_message_path)
            except Exception as e:
                print(f"Error in reading Twitter message file: {e}")

            try:
                # Post content to Twitter
                tweet_response = poster.post_tweet(tweet_message, imagepath)
                print(tweet_response)
            except Exception as e:
                print(f"Error in posting to Twitter: {e}")

