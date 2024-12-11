import os
import time
import re
import requests
import pandas as pd
from openai import OpenAI
from ExcelData import ExcelData
import openai
from dotenv import load_dotenv



class ChatGPTClient:
    """
    A client for interacting with OpenAI's GPT and DALL-E APIs, managing recipe-based workflows, 
    and processing data from Excel and text files.
    """

    def __init__(self, api_key, temperature=0.3):
        """
        Initializes the ChatGPTClient with API key and temperature settings.

        Parameters:
        api_key (str): OpenAI API key.
        temperature (float): Sampling temperature for GPT responses.
        """
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = api_key
        self.temperature = temperature
        self.content = ""
        self.recipe_folder = ""
        self.role = ""
        self.title = ""
        self.tweet = ""
        self.image_url = ""

    def set_recipe_post_folder(self, recipe_folder, post_folder):
        """
        Configures the folder paths for recipes and posts.

        Parameters:
        recipe_folder (str): Path to the recipe folder.
        post_folder (str): Path to the post folder.
        """
        self.recipe_folder = recipe_folder
        self.post_folder = post_folder
        self.picture_recipes = os.path.join(recipe_folder, "get_image.txt")
        self.tweetpost_recipes = os.path.join(recipe_folder, "get_tweet_post.txt")
        self.role_recipes = os.path.join(recipe_folder, "role.txt")
        self.set_role()

    def get_excel_values(self, google_sheet_id, range_name):
        """
        Loads data from Google Sheets into an ExcelData object.

        Parameters:
        google_sheet_id (str): The Google Sheet ID.
        range_name (str): The range of data to retrieve.
        """
        self.exda = ExcelData(google_sheet_id, range_name)

        
    def extract_data_between_dollar_signs(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Regular expression pattern to match content between $$ signs
            pattern = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
            matches = pattern.findall(content)
            return matches
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except IOError:
            print(f"Error reading file: {file_path}")
            return None
        except re.error as e:
            print(f"Regex error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def set_api_key(self, api_key):
        """
        Updates the OpenAI API key.

        Parameters:
        api_key (str): OpenAI API key.
        """
        self.api_key = api_key

    def set_temperature(self, temperature):
        """
        Updates the sampling temperature.

        Parameters:
        temperature (float): Sampling temperature for GPT responses.
        """
        self.temperature = temperature

    def set_sections(self, sections):
        self.section = sections

    def set_outline(self, outline):
        self.outline = outline

    def set_content(self, content):
        self.content = content

    def set_role(self):
        """
        Sets the role content from the role recipe file.
        """
        self.role = self.read_text_file(self.role_recipes)

    def read_text_file(self, file_path):
        # Open and read the text file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    
    def save_text_to_file(self, content, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)


    def read_and_replace(self, text_file_path, excel_file_path):
        """
        Reads a text file and replaces placeholders with values from an Excel file.

        Parameters:
        text_file_path (str): Path to the text file containing placeholders.
        excel_file_path (str): Path to the Excel file containing replacement values.

        Returns:
        str: Text content with placeholders replaced, or None on error.
        """
        try:
            # Read the text file
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
        except FileNotFoundError:
            print(f"Text file not found: {text_file_path}")
            return None
        except IOError:
            print(f"Error reading text file: {text_file_path}")
            return None

        try:
            # Read the Excel file
            data = pd.read_excel(excel_file_path)
        except FileNotFoundError:
            print(f"Excel file not found: {excel_file_path}")
            return None
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

        try:
            # Replace placeholders with values from the first row of the Excel file
            row = data.iloc[0]
            for column in data.columns:
                placeholder = f"#{column}"
                if placeholder in text_content:
                    text_content = text_content.replace(placeholder, str(row[column]))
            return text_content
        except Exception as e:
            print(f"Error during placeholder replacement: {e}")
            return None

    def read_and_replace_via_row(self, text_content, row_number):
        """
        Replaces placeholders in the text content with values from a specific row in Excel data.

        Parameters:
        text_content (str): The text content containing placeholders.
        row_number (int): The row number to fetch data from.

        Returns:
        str: Text content with placeholders replaced, or None on error.
        """
        try:
            # Assuming self.exda.data is already loaded
            data = self.exda.data

            # Get the specified row
            row = self.exda.get_the_row(row_number)
        except AttributeError:
            print("Error: 'exda' object does not have the required attribute or method")
            return None
        except IndexError:
            print(f"Row number {row_number} is out of range")
            return None
        except Exception as e:
            print(f"An error occurred during data access: {e}")
            return None

        try:
            # Replace placeholders with corresponding row values
            for column in data.columns:
                placeholder = f"#{column}"
                if placeholder in text_content:
                    text_content = text_content.replace(placeholder, str(row[column]))

            return text_content
        except KeyError:
            print("One of the columns in the row does not exist in the data")
            return None
        except Exception as e:
            print(f"An error occurred during processing: {e}")
            return None

    def split_sections(self, content):
        """
        Splits the content into sections based on '##' delimiters and stores them in a dictionary.

        Parameters:
        content (list): A list where the first element contains the content to split.

        Returns:
        dict: A dictionary where keys are section headings and values are the corresponding content.
        """
        try:
            if not content or not isinstance(content, list):
                raise ValueError("Content must be a non-empty list.")

            sections = content[0].strip().split('##')[1:]
            section_dict = {}

            for section in sections:
                lines = section.strip().split('\n')
                if not lines:
                    continue
                heading = lines[0]
                section_content = '\n'.join(lines[1:]).strip()
                section_dict[heading] = section_content

            return section_dict
        except ValueError as ve:
            print(f"Value error: {ve}")
            return None
        except IndexError:
            print("Index error: content format may be incorrect.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def extract_text_between_symbols(self, file_path, start_symbol, end_symbol):
        """
        Extracts text between specified start and end symbols in a file.

        Parameters:
        file_path (str): Path to the text file.
        start_symbol (str): The starting symbol.
        end_symbol (str): The ending symbol.

        Returns:
        list: A list of text fragments found between the specified symbols.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except IOError:
            print(f"Error reading file: {file_path}")
            return None

        try:
            # Escape any special characters in the symbols
            escaped_start_symbol = re.escape(start_symbol)
            escaped_end_symbol = re.escape(end_symbol)

            # Create a regex pattern to match text between the specified symbols
            pattern = re.compile(f'{escaped_start_symbol}(.*?){escaped_end_symbol}', re.DOTALL)

            # Find all occurrences of the pattern in the content
            matches = pattern.findall(content)

            return matches
        except re.error as e:
            print(f"Regex error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_social_media_post(self, row_number, post_type):
        """
        Generates a social media post by replacing placeholders in a recipe file with data from a specific row.

        Parameters:
        row_number (int): Row number to fetch data from.
        post_type (str): Type of post (e.g., 'twitter', 'facebook').

        Returns:
        str: The generated social media post content, or None on error.
        """

        # Determine recipe file and hashtag based on post type
        if post_type == "twitter":
            recipe_file = self.tweetpost_recipes
            hashtag = "#Tweet"
            key = "Tweet"
        elif post_type == "pinterest":
            recipe_file = self.pinpost_recipes
            hashtag = "#Pin"
            key = "Pin"
        elif post_type == "facebook":
            recipe_file = self.fbpost_recipes
            hashtag = "#FB"
            key = "FB"
        elif post_type == "Instapost":
            recipe_file = self.instapost_recipes
            hashtag = "#Insta"
            key = "Insta"
        elif post_type == "Instatags":
            recipe_file = self.tags_recipes
            hashtag = "#Insta"
            key = "Insta"
        elif post_type == "Linkedin":
            recipe_file = self.linkedin_recipes
            hashtag = "#Linkedin"
            key = "Linkedin"
        else:
            print(f"Invalid post type: {post_type}")
            return None

        try:
            # Get the row number
            row = self.exda.get_the_row(row_number)
        except AttributeError:
            print("Error: 'exda' object does not have 'get_the_row' method")
            return None
        except IndexError:
            print(f"Row number {row_number} is out of range")
            return None
        except Exception as e:
            print(f"An error occurred during row access: {e}")
            return None

        try:
            # Open the recipe
            recipe = self.read_text_file(recipe_file)
            post_query = self.replace_hashtag(recipe, hashtag, row[key])
            post_query = self.replace_hashtag(post_query, "#Title", row["Title"])
        except FileNotFoundError:
            print(f"Recipe file not found")
            return None
        except KeyError:
            print(f"Key '{key}' not found in row data")
            return None
        except Exception as e:
            print(f"An error occurred during recipe processing: {e}")
            return None

        post_content = []
        while not post_content:
            try:
                # Get the post content
                raw_content = self.query4(post_query)

                fullpath = self.post_folder + "/" + row['Day']
                raw_path = fullpath + f"/{post_type}_raw.txt"
                self.save_text_to_file(raw_content, raw_path)

                post_content = self.extract_data_between_dollar_signs(raw_path)

                if post_content:
                    post_path = fullpath + f"/{post_type}_post.txt"
                    self.save_text_to_file(post_content[0], post_path)
                else:
                    print(f"Retrying to get a non-empty {post_type} post...")
                    continue

            except FileNotFoundError:
                print(f"File not found in path: {fullpath}")
                return None
            except IndexError:
                print("No matches found in 'extract_data_between_dollar_signs'")
                return None
            except Exception as e:
                print(f"An error occurred during {post_type} post processing: {e}")
                return None

        return post_content

    def save_image_from_url(self, image_url, folder_path, file_name):
        """
        Saves an image from a URL to a specified folder. Creates the folder if it doesn't exist.

        Parameters:
        image_url (str): The URL of the image to download.
        folder_path (str): The path to the folder where the image should be saved.
        file_name (str): The name of the file to save the image as.

        Returns:
        str: A message indicating success or failure.
        """
        try:
            # Check if folder exists, if not, create it
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Get the image from the URL
            response = requests.get(image_url)
            if response.status_code == 200:
                # Save the image
                file_name = file_name + ".png"
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return f"Image saved successfully at {file_path}"
            else:
                return "Failed to download the image. Please check the URL."
        except Exception as e:
            return f"An error occurred: {e}"
        

    def get_image(self, row_number):
        """
        Generates an image using a query from a recipe file and saves it.

        Parameters:
        row_number (int): Row number to fetch data from.

        Returns:
        str: URL of the generated image, or None on error.
        """
        try:
            # Get the row number
            row = self.exda.get_the_row(row_number)
        except AttributeError:
            print("Error: 'exda' object does not have 'get_the_row' method")
            return None
        except IndexError:
            print(f"Row number {row_number} is out of range")
            return None
        except Exception as e:
            print(f"An error occurred during row access: {e}")
            return None

        try:
            # Open the recipe
            recipe = self.read_text_file(self.picture_recipes)
            image_query = self.replace_hashtag(recipe, "#Image", row['Image'])
        except FileNotFoundError:
            print(f"Recipe file not found")
            return None
        except KeyError:
            print(f"Key 'Image' not found in row data")
            return None
        except Exception as e:
            print(f"An error occurred during recipe processing: {e}")
            return None

        try:
            # Get the image
            image_url = self.query_dalle(image_query)
            self.image_url = image_url

            fullpath = self.post_folder + "/" + row['Day']
            self.save_image_from_url(image_url, fullpath, "image")

            image_url_path = fullpath + "/image_url.txt"
            self.save_text_to_file(image_url, image_url_path)
        except FileNotFoundError:
            print(f"File not found in path: {fullpath}")
            return None
        except Exception as e:
            print(f"An error occurred during image processing: {e}")
            return None

        return image_url

    def get_twitter_post(self, Row_Number):
        """
        Fetches a Twitter post based on a given row number from a data source.

        Parameters:
        Row_Number (int): The row number to retrieve the Twitter post data from.

        Returns:
        list: A list of processed Twitter post data or None if an error occurs.
        """
        try:
            # Get the row data based on the provided row number
            row = self.exda.get_the_row(Row_Number)
        except AttributeError:
            print("Error: 'exda' object does not have 'get_the_row' method")
            return None
        except IndexError:
            print(f"Row number {Row_Number} is out of range")
            return None
        except Exception as e:
            print(f"An error occurred during row access: {e}")
            return None

        try:
            # Read and process the tweet post recipe
            recipe = self.read_text_file(self.tweetpost_recipes)
            tweet_post_query = self.replace_hashtag(recipe, "#Tweet", row['Tweet'])
        except FileNotFoundError:
            print("Recipe file not found")
            return None
        except KeyError:
            print("Key 'Tweet' not found in row data")
            return None
        except Exception as e:
            print(f"An error occurred during recipe processing: {e}")
            return None

        try:
            # Process the Twitter post content
            tweet_raw = self.query4(tweet_post_query)

            fullpath = f"{self.post_folder}/{row['Day']}"
            tweet_raw_path = f"{fullpath}/tweet_raw.txt"
            self.save_text_to_file(tweet_raw, tweet_raw_path)

            tweetpost = self.extract_data_between_dollar_signs(tweet_raw_path)
            self.tweet = tweetpost

            tweet_path = f"{fullpath}/tweet_post.txt"
            self.save_text_to_file(tweetpost[0], tweet_path)
        except FileNotFoundError:
            print(f"File not found in path: {fullpath}")
            return None
        except IndexError:
            print("No matches found in 'extract_data_between_dollar_signs'")
            return None
        except Exception as e:
            print(f"An error occurred during Twitter post processing: {e}")
            return None

        return tweetpost

    def replace_hashtag(self, text, hashtag, replacement):
        """
        Replaces a specified hashtag with a given replacement string in the provided text.

        Parameters:
        text (str): The text containing the hashtag.
        hashtag (str): The hashtag to be replaced (including the '#' symbol).
        replacement (str): The string to replace the hashtag with.

        Returns:
        str: The text with the hashtag replaced by the replacement string.
        """
        updated_text = text.replace(hashtag, replacement)
        return updated_text

    def query(self, content):
        """
        Sends a query to OpenAI's GPT-3.5 API and returns the generated response.

        Parameters:
        content (str): The content to send to the GPT-3.5 model.

        Returns:
        str: The generated text response.
        """
        client = OpenAI(api_key=self.api_key)
        self.set_content(content)

        time.sleep(10)
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.role},
                        {"role": "user", "content": self.content},
                    ],
                    temperature=self.temperature
                )
                generated_text = response.choices[0].message.content
                return generated_text
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)
                time.sleep(30)
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
                time.sleep(30)
            except openai.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
                print(f"Error: {e}. Retrying in 30 seconds...")
                time.sleep(30)

    def query4(self, content):
        """
        Sends a query to OpenAI's GPT-4 API and returns the generated response.

        Parameters:
        content (str): The content to send to the GPT-4 model.

        Returns:
        str: The generated text response.
        """
        client = OpenAI(api_key=self.api_key)
        self.set_content(content)

        time.sleep(10)
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": self.role},
                        {"role": "user", "content": self.content},
                    ],
                    temperature=self.temperature
                )
                generated_text = response.choices[0].message.content
                return generated_text
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)
                time.sleep(30)
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
                time.sleep(30)
            except openai.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
                print(f"Error: {e}. Retrying in 30 seconds...")
                time.sleep(30)

    def query_dalle(self, content):
        """
        Sends a query to OpenAI's DALL-E API to generate an image based on the given prompt.

        Parameters:
        content (str): The text prompt for image generation.

        Returns:
        str: The URL of the generated image.
        """
        client = OpenAI(api_key=self.api_key)
        self.set_content(content)

        time.sleep(10)
        while True:
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=content,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                return image_url
            except openai.error.OpenAIError as e:
                print(f"Error: {e}. Retrying in 30 seconds...")
                time.sleep(30)
    
   