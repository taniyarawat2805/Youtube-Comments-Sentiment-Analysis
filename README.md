# YouTube Comment Analyzer

## Overview
YouTube Comment Analyzer is a Python application that fetches comments from a specified YouTube video using the YouTube Data API, processes the comments to identify the most common words, and displays these insights in a user-friendly graphical interface built with Tkinter.

## Key Features
- Fetches comments from a YouTube video using the YouTube Data API.
- Processes comments to identify and count the most common words.
- Supports text processing for English, Hindi, and Hinglish comments by filtering out stopwords using NLTK.
- Presents the analysis results in a GUI window with the video title, published date, and top 20 most common words.
- Utilizes a list of stopwords from a text file for Hindi and Hinglish text processing
  1. [stop_hinglish.txt](https://github.com/taniyarawat2805/Youtube-Comments-Sentiment-Analysis/blob/main/stop_hinglish.txt).
  2. [hindiStopWord.txt](https://github.com/taniyarawat2805/Youtube-Comments-Sentiment-Analysis/blob/main/hindiStopWords.txt)

You can customize the path to `stop_hinglish.txt` based on where you store it in your project repository.

## Technologies Used
- Python
- Pandas for data manipulation
- NLTK (Natural Language Toolkit) for natural language processing
- Tkinter for building the graphical user interface
- Google API Client for interacting with the YouTube Data API

## Getting Started
### Prerequisites
- Python 3.x installed
- Dependencies installed (use `pip install -r requirements.txt`)

### Installation
1. Repository:

   ```bash
   git clone https://github.com/taniyarawat2805/Youtube-Comments-Sentiment-Analysis
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. Usage:

- Replace `DEVELOPER_KEY` in `main.py` with your YouTube Data API key.
- Set the `videoID` variable in `main.py` to the ID of the YouTube video you want to analyze.
- Run the script: [CommentAnalyzer.py](https://github.com/taniyarawat2805/Youtube-Comments-Sentiment-Analysis/blob/main/commentAnalyzer.py) 

  ```bash
   https://github.com/taniyarawat2805/Youtube-Comments-Sentiment-Analysis/blob/main/commentAnalyzer.py
  ```
- The GUI window will display the video details, fetched comments count, and the top 20 most common word.
  


