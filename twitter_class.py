import tweepy
from PIL import Image
from io import BytesIO

class TwitterPoster:
    """
    A class to handle Twitter posting, including authentication and image processing.
    """

    def __init__(self):
        """
        Initialize the TwitterPoster with default values.
        """
        self.tweet = ""
        self.title = ""
        self.extra_line = "\nCheck out the link in Bio for more info"
        self.check_comment = "\nCheck out the link in the comments for more info"
        self.twitter_api = None
        self.twitter_client = None

    def authenticate(self, client_id, client_secret, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token):
        """
        Authenticate with Twitter using the provided credentials.

        Args:
            client_id (str): Twitter client ID.
            client_secret (str): Twitter client secret.
            consumer_key (str): Twitter consumer key.
            consumer_secret (str): Twitter consumer secret.
            access_token (str): Twitter access token.
            access_token_secret (str): Twitter access token secret.
            bearer_token (str): Twitter bearer token.

        Raises:
            Exception: If there is an error during authentication.
        """
        try:
            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
            self.twitter_api = tweepy.API(auth)

            self.twitter_client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
        except Exception as e:
            raise Exception(f"Error during Twitter authentication: {e}")

    def save_text_to_file(self, content, file_path):
        """
        Save text content to a file.

        Args:
            content (str): The text content to save.
            file_path (str): Path to the file where content will be saved.

        Raises:
            Exception: If there is an error while saving the file.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise Exception(f"Error while saving text to file: {e}")

    def post_tweet(self, message, image_path):
        """
        Post a tweet with a message and an optional image.

        Args:
            message (str): The message to be posted.
            image_path (str): Path to the image to be posted with the message.

        Returns:
            tweepy.Client: The Twitter client instance used for the post.

        Raises:
            Exception: If there is an error during the posting process.
        """
        try:
            # Verify credentials
            if not self.twitter_api.verify_credentials().screen_name:
                raise Exception("Twitter credentials verification failed.")

            # Process the image
            photo = Image.open(image_path)
            basewidth = 320
            wpercent = (basewidth / float(photo.size[0]))
            height = int((float(photo.size[1]) * float(wpercent)))
            photo = photo.resize((basewidth, height), Image.Resampling.LANCZOS)

            # Save processed image to a BytesIO object
            image_io = BytesIO()
            photo.save(image_io, format='PNG')
            image_io.seek(0)

            # Upload image and create tweet
            media = self.twitter_api.media_upload(image_path)
            self.twitter_client.create_tweet(text=message, media_ids=[media.media_id])
            self.tweet = message
            return self.twitter_client

        except Exception as e:
            raise Exception(f"Error while posting tweet: {e}")
