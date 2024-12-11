# Twitter Poster using Google Sheet 

Here’s a README.md file for your project:


# Social Media Poster with ChatGPT and Twitter API Integration

This project automates the process of posting content to social media platforms, specifically Twitter, by fetching data from Google Sheets and utilizing ChatGPT for content generation. 

---

## Features

- **Twitter API Integration**: Posts content to Twitter with images and text.
- **Google Sheets Integration**: Reads post data such as title, link, and date from a Google Sheet.
- **ChatGPT Integration**: Generates social media content for Twitter posts.
- **Scheduled Posting**: Posts content based on dates specified in the Google Sheet.
- **Error Handling**: Includes mechanisms for logging and handling exceptions during the process.

---

## Prerequisites

1. **Python**: Ensure Python 3.7 or later is installed.
2. **Environment Variables**: Create a `.env` file in the project directory containing API keys and credentials (see example below).
3. **Google Cloud Project**: Set up a Google Cloud project with Google Sheets API enabled and generate a service account JSON file.
4. **Dependencies**: Install required Python libraries using the `requirements.txt` file.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-repository-url.git
cd your-project-folder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory with the following structure:
```env
# Twitter API Credentials
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# Google Sheets Information
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_RANGE=Sheet1!A1:J
GOOGLE_SERVICE_ACCOUNT_JSON=your_google_service_account_file.json

# ChatGPT API Key
CHATGPT_API=your_chatgpt_api_key
```

### 4. Add Google Service Account JSON File
Here’s an updated section for the README.md file detailing how to add and configure the Google Sheet:

https://mljar.com/blog/authenticate-python-google-sheets-service-account-json-credentials/
---

## 4a. Adding the Google Sheet

The script fetches post data from a Google Sheet. The Google Sheet must follow a specific structure for the code to function correctly.

### Required Column Names

Ensure your Google Sheet contains the following column names in the first row:

| **Column Name** | **Description**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| `Day`            | A unique identifier for the post, typically numeric (e.g., 1, 2, 3, etc.).    |
| `Date`           | The scheduled posting date in the format `%m/%d/%Y` (e.g., 12/8/2024).         |
| `Title`          | The title of the post.                                                        |
| `Image`          | A description of the image to be used or path to the image file.              |
| `Tweet`          | The content of the tweet (text message).                                      |
| `Link`           | The URL to include in the post.                                               |

### Example Google Sheet Data

| Day | Date       | Title                                   | Image                                                              | Tweet                                                   | Link               |
|-----|------------|-----------------------------------------|--------------------------------------------------------------------|---------------------------------------------------------|--------------------|
| 1   | 12/8/2024  | Warum Ihre Website Ihr wichtigstes Asset ist | Ein Laptop mit einer perfekt gestalteten Website und Wachstumsdiagrammen. | Ihre Website sollte verkaufen, informieren und beeindrucken. #WebDesign | brandovise.com    |
| 2   | 12/9/2024  | 5 Merkmale einer großartigen Website     | Eine Website mit klarer Navigation, moderner Typografie und schneller Ladezeit. | Eine Website, die performt: Die 5 Must-haves für Ihre digitale Präsenz. #WebDevelopment | brandovise.com    |
| 3   | 12/10/2024 | Wie ein klares Design den Erfolg steigert | Ein minimalistisches Website-Layout mit Fokus auf Benutzerfreundlichkeit. | Klare Designs, große Wirkung – optimieren Sie Ihre Website noch heute. #MinimalDesign | brandovise.com    |
| 4   | 12/11/2024 | Warum Geschwindigkeit zählt             | Eine Stoppuhr vor einem Laptop mit einer schnellen Ladezeit-Anzeige. | Geschwindigkeit ist der Schlüssel – Ihre Website muss blitzschnell sein! #FastWeb | brandovise.com    |
| 5   | 12/12/2024 | Mobilfreundlichkeit ist ein Muss         | Ein Smartphone mit einer responsiven Website, die sich perfekt anpasst. | 75% der Nutzer surfen mobil – passen Sie Ihre Website an! #MobileFriendly | brandovise.com    |

### Important Notes

1. **Column Names Must Match**: The column names in the Google Sheet must match exactly as shown above (case-sensitive). If column names differ, the script will not work correctly.
2. **Date Format**: The `Date` column must use the format `%m/%d/%Y` (e.g., `12/8/2024`) to ensure compatibility with the script.
3. **Sheet ID and Range**:
   - Replace `GOOGLE_SHEET_ID` in the `.env` file with the ID of your Google Sheet.
   - Set the `GOOGLE_SHEET_RANGE` to the range containing your data (e.g., `Sheet1!A1:J`).

---

### How to Share the Google Sheet with the Service Account

1. Open your Google Sheet.
2. Click **Share** in the top-right corner.
3. Share the sheet with the email address associated with your Google service account (found in the JSON file).

---

By following these instructions, your Google Sheet will be correctly configured for the script to read data and generate posts successfully.


### 5. Organize Recipe and Post Folders
Create the following folders in the root directory:
- `recipe/`
- `post/`

These folders will be used by the script to manage data and content.

---

## How to Run the Script

1. Ensure all environment variables are set and dependencies are installed.
2. Run the script:
```bash
python your_script_name.py
```
3. The script will fetch data from the Google Sheet, generate content using ChatGPT, and post it to Twitter.

---

## Environment Variable Details

| Variable                     | Description                                            |
|------------------------------|--------------------------------------------------------|
| `TWITTER_CLIENT_ID`          | Twitter API client ID                                  |
| `TWITTER_CLIENT_SECRET`      | Twitter API client secret                              |
| `TWITTER_CONSUMER_KEY`       | Twitter consumer key                                   |
| `TWITTER_CONSUMER_SECRET`    | Twitter consumer secret                                |
| `TWITTER_ACCESS_TOKEN`       | Twitter access token                                   |
| `TWITTER_ACCESS_TOKEN_SECRET`| Twitter access token secret                            |
| `TWITTER_BEARER_TOKEN`       | Twitter bearer token                                   |
| `GOOGLE_SHEET_ID`            | ID of the Google Sheet used for data                  |
| `GOOGLE_SHEET_RANGE`         | Range of cells to read from the Google Sheet           |
| `GOOGLE_SERVICE_ACCOUNT_JSON`| Path to the Google service account JSON file           |
| `CHATGPT_API`                | API key for accessing the OpenAI ChatGPT API          |

---

## Customization

- **Social Media Platforms**: Update the `post_in` list to include other platforms.
- **Folder Structure**: Modify the `recipe/` and `post/` folder paths if necessary.
- **Date Format**: Ensure the date format in the Google Sheet matches `%m/%d/%Y`.

---

## Troubleshooting

- Ensure that the `.env` file and Google service account JSON file are properly configured.
- Verify your API keys and tokens are valid.
- Check that the required permissions are granted for the Google Sheets and Twitter APIs.
- Install any missing Python dependencies listed in `requirements.txt`.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

- Jibran Shahid
- jshahid [at] brandovise.com

---

Happy posting! 🚀
```

### Steps to finalize:
1. Replace placeholders like `your_client_id` and `your_script_name.py` with actual values.
2. Add a `requirements.txt` file listing all Python dependencies if not already done.
3. Include additional notes if the project grows in complexity.
 
