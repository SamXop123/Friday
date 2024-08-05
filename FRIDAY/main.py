import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<your news api>"


def speak_old(text):
    engine.say(text)  
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def aiProcess(command):
    client = OpenAI(api_key="your openai API",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Reply in short."},
        {"role": "user", "content": command}
    ]
    )
    return completion.choices[0].message.content


def processCommand(c):
    print(c)
    commands = {
        "open google": "https://google.com",
        "open youtube": "https://youtube.com",
        "open gmail": "https://mail.google.com/",
        "open linkedin": "https://linkedin.com",
        "open whatsapp": "https://web.whatsapp.com",
        "open edx": "https://home.edx.org"
    }

    for command, url in commands.items():
        if command in c.lower():
            webbrowser.open(url)
            speak(f"Opening {command.split(' ')[1].capitalize()}")
            return

    if c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:])
        link = music_library.music.get(song, None)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
        return

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 
        
        

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        
        # Listen for the wake word "jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=10, phrase_time_limit=1)

            word = r.recognize_google(audio)

            if(word.lower() == "jarvis"):
                speak("Ya")

                # Listen for command
                with sr.Microphone() as source:
                    print("jarvis Active...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=3)
                    command = r.recognize_google(audio)

                    processCommand(command)
        
        except sr.RequestError as e:
            speak("Sorry, I couldn't reach the speech recognition service.")

        except Exception as e:
            print("Error; {0}".format(e))

    