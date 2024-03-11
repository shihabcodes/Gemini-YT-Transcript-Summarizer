import os
import re

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Google GenerativeAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
prompt = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise summary. Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. Let's dive into the provided transcript and extract the vital details for our audience."""


# Function to extract transcript details from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        match = re.match(
            r"^(http|https)://www\.youtube\.com/(v=|watch\?v=)([a-zA-Z0-9_-]+)", youtube_video_url)
        if match:

            video_id = match.group(3)
            print(video_id)
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([item["text"] for item in transcript_text])
            return transcript
        else:
            raise ValueError("Invalid YouTube URL format.")
    except ConnectionError:
        raise ConnectionError("Network error occurred.")
    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Streamlit UI
st.title(
    "Gemini YouTube Transcript Summarizer: Extract Key Insights from YouTube Videos"
)
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(
        f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to trigger summary generation
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate summary using Gemini Pro
        summary = generate_gemini_content(transcript_text, prompt)

        # Display summary
        st.markdown("## Detailed Notes:")
        st.write(summary)
