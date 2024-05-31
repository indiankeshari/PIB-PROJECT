import requests
from bs4 import BeautifulSoup

url = input("Web Link : ")
# for testing you can use url = "https://pib.gov.in/PressReleasePage.aspx?PRID=2012535"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all('p')

output = ""

for x in articles:
    text = x.text
    if x.find('blockquote', class_='twitter-tweet tw-align-center'):
        continue
    output = output + text
    if(output[-1]=="" or output[-2]==""):
        break

user_input = output.split(".")


#=============================================================

import os
import base64
import requests
#==============================================================

def fun(text,A):
    api_key   = "sk-zEMiCd3KjeVL9sHKZKMYmYmC6"
    api_host  = "https://api.stability.ai"
    engine_id = "stable-diffusion-v1-6"
    #==============================================================
    if api_key is None:
        raise Exception("Missing Stability API key.")
    
    #==============================================================
    response = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image",headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },json={
            "text_prompts": [
                {
                    "text": text
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        
    })
    
    #==============================================================
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    #==============================================================
    data = response.json()
    #==============================================================
    for i, image in enumerate(data["artifacts"]):
        a=str(A)
        with open(f"./{a}image_{i}.png","wb") as f:
            f.write(base64.b64decode(image["base64"]))
            
from gtts import gTTS
import pygame
from translate import Translator



# Define a dictionary of languages and their corresponding language codes
languages = {
        "Hindi": "hi",
        "Urdu": "ur",
        "Gujarati": "gu",
        "Marathi": "mr",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Tamil": "ta",
        "Bengali": "bn",
        
}

# Display the list of available languages
print("Available languages:")
for lang, code in languages.items():
    print(f"{lang}: {code}")

# Prompt the user to select a language
selected_language = input("Enter the language code from the list above: ").strip()  # Remove leading/trailing whitespace
    
    
def funspeak(text,A):    
    # Check if the selected language is in the dictionary
    if selected_language in languages.values():
        # Input text in English
        input_text = text

        # Translate English to the selected language using the translate library
        translator = Translator(to_lang=selected_language)
        translated_text = translator.translate(input_text)

        # Create a gTTS object for the translated text
        language = selected_language
        slow = False  # Set to True to slow down the speech (optional)

        # Create a gTTS object for the translated text
        tts = gTTS(text=translated_text, lang=language, slow=slow)
        
        # Save the translated speech to an audio file
        a=str(A)
        output_filename = f"output{a}_{selected_language}.mp3"
        tts.save(output_filename)

        # Initialize pygame
        pygame.init()

        # Load and play the translated audio file
        pygame.mixer.music.load(output_filename)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("Invalid language code. Please select a language code from the list.")
        
        
A=0
for i in user_input:
    fun(i,A)
    
    funspeak(i,A)
    
    A=A+1
    print(i)

def combinePicWithAudio(A):
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

    # Path to the image file (change this to your image file)
    a=str(A)
    image_path = f"C:/Users/Aman/OneDrive/Desktop/Programs/pythonProject/{a}image_0.png"

    # Path to the MP3 audio file (change this to your MP3 file)
    audio_path = f"C:/Users/Aman/OneDrive/Desktop/Programs/pythonProject/output{a}_{selected_language}.mp3"

    # Output video file name
    output_video_path = f'PicWithAudio{a}.mp4'

    # Load the image and audio
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the duration of the image clip to match the duration of the audio clip
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Set the frame rate (fps) for the video
    image_clip = image_clip.set_fps(24)  # Adjust the frame rate as needed

    # Concatenate the image and audio clips
    final_clip = concatenate_videoclips([image_clip.set_audio(audio_clip)], method="compose")

    # Write the final video with audio
    final_clip.write_videofile(output_video_path, codec='libx264', fps=24)  # Set the desired frame rate

    print(f"Video '{output_video_path}' has been created.")
    
length=len(user_input)

for i in range (0,length):
    combinePicWithAudio(i)


from moviepy.editor import *
videos = []
for i in range(0,length):
    temp = VideoFileClip(f"PicWithAudio{i}.mp4")
    videos.insert(i, temp)

final_video = concatenate_videoclips(videos, method="compose")
final_video.write_videofile("FinalVideo.mp4")