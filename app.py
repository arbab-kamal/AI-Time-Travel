import os
import openai
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import requests
from io import BytesIO

# Load environment variables
load_dotenv()

# Retrieve API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to generate story using GPT-3.5
def generate_story(year, place):
    """
    Generate a story using OpenAI's GPT-3.5.
    """
    try:
        prompt = f"Write a vivid and imaginative story set in {place} during the year {year}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a creative storyteller."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating story: {e}"

# Function to generate image using OpenAI DALL-E
def generate_image(year, place):
    """
    Generate an image using OpenAI's DALL-E.
    """
    try:
        prompt = f"A scene from {place} in the year {year}, highly detailed, artistic, and imaginative."
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        return f"Error generating image: {e}"

# Streamlit App
st.title("AI Time Travel")
st.subheader("Enter a year and place, and let AI create a story and an image for you!")

# User input
year = st.text_input("Enter the year (e.g., 1889, 2050):")
place = st.text_input("Enter a place (e.g., Paris, Mars):")

# Generate button
if st.button("Generate"):
    if year and place:
        with st.spinner("Generating your story and image..."):
            try:
                # Generate story
                story = generate_story(year, place)
                
                # Generate image
                image_url = generate_image(year, place)
                
                # Display results
                st.markdown("### Story")
                st.write(story)
                
                st.markdown("### Image")
                if "Error" not in image_url:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=f"{place} in {year}")
                else:
                    st.error(image_url)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter both a year and a place!")
