import os
import sys
import pyttsx3
import speech_recognition as sr

# Initialize engine globally to avoid re-initialization issues
engine = pyttsx3.init()

def set_deep_male_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Daniel" in voice.name:
            engine.setProperty('voice', voice.id)
            return
    for voice in voices:
        if "male" in voice.name.lower() or "male" in str(voice.gender).lower():
            engine.setProperty('voice', voice.id)
            return

set_deep_male_voice()
is_speaking = False

def speak(text):
    global is_speaking
    if "{" in text and "}" in text and "status" in text:
        text = "Task completed."
    
    print(f"JARVIS: {text}")
    is_speaking = True

    try:
        if sys.platform == "darwin":  # macOS
            try:
                clean_text = text.replace('"', '\\\"').replace("'", "")
                os.system(f'say "{clean_text}"')
                return
            except Exception as e2:
                print(f"TTS Fallback Error: {e2}")

        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    finally:
        is_speaking = False

def listen():
    global is_speaking
    if is_speaking:
        return "none"

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio)
            return query.lower()
        except Exception:
            return "none"