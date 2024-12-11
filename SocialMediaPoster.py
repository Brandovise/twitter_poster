import facebook
import requests
from pyfacebook import GraphAPI
from imgurpython import ImgurClient
from PIL import Image
import tweepy
from io import StringIO
from io import BytesIO
from pinterest.organic.pins import Pin
import pinterest.client as cli
import pinterest
import base64
import webbrowser


import json

import os
import re





class SocialMediaPoster:
    def __init__(self): # , ig_access_token, ig_user_id, pin_access_token):
        
        #FB & Insta
        self.fb_post = ""
        self.instapost = ""

        # imgueclient
        self.imagelink = ""
        self.imagepath = ""
        

        # Twitter
        self.tweet = ""

        ## Linkedin
        self.linkedin_post = ""

        ## Title
        self.title = ""
        self.ExtraLine = "\nCheck out link in Bio for More info"
        self.CheckComment = "\nCheck out link in the comments for More info"


    def auth_img(self,client_id, client_secret):
        try:
            self.imgur = ImgurClient(client_id, client_secret)
        except Exception as e:
            print(f"Error in auth_img: {e}")

    def auth_fb(self, fb_access_token, FB_APP_ID, FB_APP_SECRET, instapage, fb_page, fb_group ):
        try:
            # FB & Insta Keys Login
            self.fb_access_token = fb_access_token
            self.FB_APP_ID = FB_APP_ID
            self.FB_APP_SECRET = FB_APP_SECRET
            self.instapage = instapage
            self.fb_page = fb_page
            self.fb_group = fb_group
            self.fb_api = GraphAPI(app_id=self.FB_APP_ID, app_secret=self.FB_APP_SECRET, access_token=self.fb_access_token)

        except Exception as e:
            print(f"Error in auth_fb: {e}")
        

    def auth_twitter(self, x_client_id, x_client_secret, x_consumer_key, x_consumer_secret, x_access_token,x_access_token_secret, x_bearer_token):
        try:  

            # Twitter
            self.x_client_id = "NUlLcWQxZGpnVlYwcFhiMXgtdHY6MTpjaQ"
            self.x_client_secret = "rGUxDNrWUyTHhzdM-nMMlIVv80166DNgXvwbTzbvtJ2LGGDpHO"
            self.x_consumer_key = "Py5StomTT59zRN5fKKRRbenf3"
            self.x_consumer_secret = "weikQhHNnZv7g6NUgcx8TUfnxWmZuXExLiJkOjheWIpKqKXqtJ"
            self.x_access_token = "1858531134080249856-puwIo3BZ2MdZnaKgP0DS7TvW322LUN"
            self.x_access_token_secret = "d6v1QM3ouY92RhK3o6RE4pFPZh86CYUITe6KoIfRg7mmz"
            self.x_bearer_token = "AAAAAAAAAAAAAAAAAAAAADqOxAEAAAAApogo%2BINBZ7NylAthT%2BsmyXv2Nls%3DNGDPjV2aRiTZ0JgigiJW3MLsZjDcz2uJjQB3QNhYR693vzBCJr"

            # # Twitter
            # self.x_client_id = x_client_id
            # self.x_client_secret = x_client_secret
            # self.x_consumer_key = x_consumer_key
            # self.x_consumer_secret = x_consumer_secret
            # self.x_access_token = x_access_token
            # self.x_access_token_secret = x_access_token_secret
            # self.x_bearer_token = x_bearer_token

            auth = tweepy.OAuth1UserHandler(
                self.x_consumer_key, self.x_consumer_secret, self.x_access_token, self.x_access_token_secret
            )
            self.twitter2 = tweepy.API(auth)

            #self.twitter3 = tweepy.Client(bearer_token=self.x_bearer_token)

            self.twitter3 = tweepy.Client(
                consumer_key=self.x_consumer_key, consumer_secret=self.x_consumer_secret,
                access_token=self.x_access_token, access_token_secret=self.x_access_token_secret
            )
        except Exception as e:
            print(f"Error in auth_twitter: {e}")



    def save_text_to_file(self, content, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            print(f"Error in save_text_to_file: {e}")

    def upload_an_image(self, imagepath): 

        Image_Link_1 = ""
        try:
            Image_link = self.imgur.upload_from_path(imagepath)
            self.imagepath = imagepath
            Image_Link_1 = "https://imgur.com/{id}.jpg".format(id = Image_link['id'])
            self.imagelink = Image_Link_1

            imagelinktxt = self.imagepath.replace('png', 'txt')
            self.save_text_to_file(Image_Link_1, imagelinktxt)

            return Image_Link_1
    
        except Exception as e:
            print(f"Error in upload_an_image: {e}")
        

    def post_on_page(self, imageurl,  message):
        data = ""

        try:
            data = self.fb_api.post_object(
                object_id=self.fb_page,
                connection="photos",
                params={
                "fields": "id"},
                data={"message":  message, "url": imageurl}
            )
            self.fb_post = message
            print(data)

            self.fb_data = data

            # {'id': 'xxx', 'message': 'This is a test message by api', 'created_time': '2022-06-01T03:49:36+0000', 'from': {'name': 'xx', 'id': 'xxxx'}}
            return data
        except Exception as e:
            print(f"Error in post_on_page: {e}")
    
    def post_on_group(self, imageurl,  message):
        data = ""

        try:
            data = self.fb_api.post_object(
                object_id=self.fb_group,
                connection="photos",
                params={
                "fields": "id"},
                data={"message":  message, "url": imageurl}
            )


            self.fb_post = message
            print(data)

            self.fb_data = data
            # {'id': 'xxx', 'message': 'This is a test message by api', 'created_time': '2022-06-01T03:49:36+0000', 'from': {'name': 'xx', 'id': 'xxxx'}}
            return data
        
        except Exception as e:
            print(f"Error in post_on_group: {e}")
    
    
    def post_a_fb_comment(self, id,  message):
        
        try:
            self.fb_api.post_object(
                object_id=id,
                connection="comments",
                params={
                "fields": "id"},
                data={"message":  message}
            )
        except Exception as e:
            print(f"Error in post_a_fb_comment: {e}")

    def post_on_insta(self, message, tags):
        
        try:
            Complete_post = message + "\n\n" + tags
            data = self.fb_api.post_object(
                object_id=self.instapage,
                connection="media",
                params={
                    "image_url": self.imagelink,  # replace with your image url.
                    "caption": Complete_post,  # replace with your caption for the media.
                },
            )
            print(data)
            # {'id': '17952987976782688'}
            # Get your container id.
            container_id = data["id"]

            # Then publish the container.
            publish_data = self.fb_api.post_object(
                object_id= self.instapage,
                connection="media_publish",
                params={
                    "creation_id": container_id,
                },
            )
            print(publish_data)
            self.instapost = Complete_post
        
        except Exception as e:
            print(f"Error in post_on_insta: {e}")    

    def post_on_twitter(self,message):
        try:
            print(self.twitter2.verify_credentials().screen_name)
            
            # Load and process the image
            photo = Image.open(self.imagepath)
            basewidth = 320
            wpercent = (basewidth / float(photo.size[0]))
            height = int((float(photo.size[1]) * float(wpercent)))
            photo = photo.resize((basewidth, height), Image.Resampling.LANCZOS)

            # Save processed image to a BytesIO object
            image_io = BytesIO()
            photo.save(image_io, format='PNG')
            image_io.seek(0)

            # Upload image
            media = self.twitter2.media_upload(self.imagepath)
            self.twitter3.create_tweet(text=message,  media_ids=[media.media_id])
            self.tweet = message
            return self.twitter3
        except Exception as e:
            print(f"Error in post_on_twitter: {e}")  

 