import time
from ChatGPTCleint import ChatGPTClient
from SocialMediaPoster import SocialMediaPoster


# Declare API keys

fb_access_token = ""
ig_access_token = ""
ig_user_id = ""
pin_access_token = ""


# Initialize the class with your access tokens, Instagram User ID, and Pinterest Access Token
poster = SocialMediaPoster(fb_access_token, ig_access_token, ig_user_id, pin_access_token)

# Initilize the ChatGPT Client instance of the ChatGPTClient class
client = ChatGPTClient()

# Usage:
# Row_number = 2
# Create an instance of the ChatGPTClient class

for row_number in range(0, len(client.exda.data)): # Start with the number shown in the excel 
    
    ## get the image 
    client.get_image(row_number)
    print(f"Image has beeen received for {client.exda.keyword1[row_number]}")

    ## get the insta post


    ## get the hashtags


    ## get the FB post


    ## get the Pin Post

    # # Post to Facebook
    # fb_response = poster.post_to_facebook('path_to_your_image.jpg', 'Your message')
    # print(fb_response)

    # # Post to Instagram
    # ig_response = poster.post_to_instagram('url_to_your_image', 'Your caption')
    # print(ig_response)

    # # Post to Pinterest
    # pin_response = poster.post_to_pinterest('your_board_id', 'url_to_your_image', 'Your note', 'Your link')
    # print(pin_response)
    k = 1
    client.get_excel_values()





