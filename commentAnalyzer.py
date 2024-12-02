import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from googleapiclient.discovery import build
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import matplotlib.pyplot as plt

# Download the NLTK stopwords corpus and VADER lexicon
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('punkt_tab')

# Your YouTube API key
DEVELOPER_KEY = "AIzaSyCaVm9vG9yWNgd1xPn6899IIblPIWJweeY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# ID of the video you want to analyze
videoID = "5WmBt6BBUzs"

# Initialize YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_comments(videoID):
    """Fetches comments from a given YouTube video."""
    comments = []
    try:
        # Request comments
        response = youtube.commentThreads().list(
            part="snippet", videoId=videoID, textFormat="plainText", maxResults=100
        ).execute()

        while response:
            # Extract comment text
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
            
            # Check for more comments (pagination)
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                    part="snippet", videoId=videoID, textFormat="plainText", maxResults=100,
                    pageToken=response['nextPageToken']
                ).execute()
            else:
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return comments

def get_video_details(videoID):
    """Fetches the title and publish date of a YouTube video."""
    try:
        response = youtube.videos().list(part="snippet", id=videoID).execute()
        video_details = response['items'][0]['snippet']
        title = video_details['title']
        published_at = video_details['publishedAt']
        published_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
        return title, published_date
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def read_stopwords(file_path):
    """Reads stopwords from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Paths to stopwords files
hinglish_stopwords_file = 'stop_hinglish.txt'
hindi_stopwords_file = 'hindiStopWords.txt'

# Load stopwords
hinglish_stopwords = read_stopwords(hinglish_stopwords_file)
hindi_stopwords = read_stopwords(hindi_stopwords_file)
english_stopwords = set(stopwords.words('english'))

# Combine all stopwords
all_stopwords = english_stopwords.union(hinglish_stopwords).union(hindi_stopwords)

# Fetch comments and video details
video_comments = get_comments(videoID)
video_title, video_date = get_video_details(videoID)

if isinstance(video_comments, list):
    print(f"Fetched {len(video_comments)} comments from video ID: {videoID}")

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Analyze sentiment
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}

    for comment in video_comments:
        score = sia.polarity_scores(comment)
        if score['compound'] >= 0.05:
            sentiments['positive'] += 1
        elif score['compound'] <= -0.05:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1

    total_comments = len(video_comments)
    positive_percent = (sentiments['positive'] / total_comments) * 100
    neutral_percent = (sentiments['neutral'] / total_comments) * 100
    negative_percent = (sentiments['negative'] / total_comments) * 100

    # Process comments
    all_comments = ' '.join(video_comments)
    words = nltk.word_tokenize(all_comments.lower())
    words = [word for word in words if word.isalpha() and word not in all_stopwords]
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(20)

    def show_pie_chart():
        """Displays a pie chart of sentiment analysis results."""
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [positive_percent, neutral_percent, negative_percent]
        colors = ['#00ff00', '#ffcc00', '#ff3333']
        explode = (0.1, 0, 0)  # Highlight the positive segment

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=140, explode=explode, shadow=True)
        plt.title(f"Sentiment Analysis of Comments for '{video_title}'")
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.show()

    def create_window():
        """Creates a GUI window to display the most common words and sentiment analysis results."""
        window = tk.Tk()
        window.title("YouTube Comment Analysis")
        window.geometry("800x600")

        frame = ttk.Frame(window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text=f"Video Title: {video_title}",
                  font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(frame, text=f"Published Date: {video_date}",
                  font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text=f"Fetched Comments: {len(video_comments)}",
                  font=("Helvetica", 12)).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text=f"Positive Comments: {positive_percent:.2f}%",
                  font=("Helvetica", 12)).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text=f"Neutral Comments: {neutral_percent:.2f}%",
                  font=("Helvetica", 12)).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Label(frame, text=f"Negative Comments: {negative_percent:.2f}%",
                  font=("Helvetica", 12)).grid(row=5, column=0, columnspan=2, pady=5)

        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=18,
                                              font=("Helvetica", 12))
        text_area.grid(row=6, column=0, columnspan=2, pady=10)
        text_area.insert(tk.END, "Top 20 Most Common Words:\n\n")
        
        for i, (word, freq) in enumerate(most_common_words, start=1):
            text_area.insert(tk.END, f"{i}.\t{word}\t:\t{freq}\n")

        text_area.configure(state='disabled')

        pie_button = ttk.Button(frame, text="Show Sentiment Pie Chart", command=show_pie_chart)
        pie_button.grid(row=7, column=0, columnspan=2, pady=10)

        window.mainloop()

    if most_common_words:
        create_window()
    else:
        print("No comments or valid words found.")

else:
    print("Failed to fetch comments.")
