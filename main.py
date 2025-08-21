
import sounddevice as sd
import queue
import json
import pyttsx3
import webbrowser
import wikipedia
import requests
from vosk import Model, KaldiRecognizer
from datetime import datetime

# Load Vosk model
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# TTS engine
engine = pyttsx3.init()

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def speak(text):
    print("🗣️ Whispy says:", text)
    engine.say(text)
    engine.runAndWait()

# Jokes list
jokes = [
    "Why did the computer go to the doctor? Because it caught a virus!",
    "What is a robot’s favorite snack? Computer chips!",
    "Why did the math book look sad? Because it had too many problems!"
]

# Weather helper (simple, uses Open-Meteo)
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current_weather=true"  # Example: Delhi
        response = requests.get(url).json()
        temp = response["current_weather"]["temperature"]
        return f"The current temperature is {temp} degrees Celsius."
    except:
        return "Sorry, I could not fetch the weather right now."
    
# Open microphone stream
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):

    speak("Hello Mansour! I am Whispy. Say a command. Say stop to quit.")

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]
            if text:
                print("📝 Whispy heard:", text)

                if "stop" in text.lower() or "bye" in text.lower():
                    speak("Goodbye Mansour, see you soon!")
                    break

                elif "hello" in text.lower() or "hi" in text.lower():
                    speak("Hello! Nice to hear you.")

                elif "your name" in text.lower():
                    speak("My name is Whispy. I am your voice assistant.")

                elif "youtube" in text.lower() or "you tube" in text.lower():
                    speak("Opening YouTube for you!")
                    webbrowser.open("https://www.youtube.com")

                elif "github" in text.lower() or "get up" in text.lower():
                    speak("Opening GitHub for you!")
                    webbrowser.open("https://www.github.com")

                elif "facebook" in text.lower():
                    speak("Opening Facebook for you!")
                    webbrowser.open("https://www.facebook.com")

                elif "google" in text.lower():
                    speak("Opening Google for you!")
                    webbrowser.open("https://www.google.com")

                elif "time" in text.lower():
                    now = datetime.now().strftime("%H:%M")
                    speak(f"The time is {now}")

                elif "date" in text.lower():
                    today = datetime.now().strftime("%A, %B %d, %Y")
                    speak(f"Today is {today}")

                elif "joke" in text.lower():
                    import random
                    joke = random.choice(jokes)
                    speak(joke)

                elif "wikipedia" in text.lower():
                    try:
                        query = text.replace("wikipedia", "")
                        result = wikipedia.summary(query, sentences=2)
                        speak(result)
                    except:
                        speak("Sorry, I could not find anything on Wikipedia.")

                elif "weather" in text.lower():
                    weather_info = get_weather()
                    speak(weather_info)

                else:
                    speak("I heard you say " + text)