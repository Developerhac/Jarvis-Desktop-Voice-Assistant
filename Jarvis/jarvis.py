import os
import datetime
import webbrowser as wb
import random

import pyttsx3
import pyautogui
import wikipedia
import pyjokes

try:
    import speech_recognition as sr
except Exception:
    sr = None

# TTS engine init with safe voice selection
engine = pyttsx3.init()
voices = engine.getProperty("voices")
try:
    engine.setProperty("voice", voices[1].id)
except Exception:
    if voices:
        engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)
engine.setProperty("volume", 1)


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    speak("Welcome back, sir!")
    print("Welcome back, sir!")
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Hello!")
        print("Hello!")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def screenshot() -> None:
    img = pyautogui.screenshot()
    pictures = os.path.join(os.path.expanduser("~"), "Pictures")
    os.makedirs(pictures, exist_ok=True)
    path = os.path.join(pictures, "screenshot.png")
    img.save(path)
    print(f"Screenshot saved to {path}")


def takecommand():
    # try microphone first; if unavailable fall back to typed input
    if sr is None:
        print("SpeechRecognition not installed. Falling back to typed input.")
        return input("Type your command: ").strip().lower()
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("Network error while recognizing speech.")
            return ""
    except (AttributeError, OSError, sr.RequestError, ModuleNotFoundError):
        print("Microphone not available. Falling back to typed input.")
        try:
            return input("Type your command: ").strip().lower()
        except EOFError:
            return ""


def play_music(song_name=None) -> None:
    music_dir = os.path.join(os.path.expanduser("~"), "Music")
    if not os.path.isdir(music_dir):
        speak("No music directory found.")
        print("No music directory found at", music_dir)
        return
    files = [f for f in os.listdir(music_dir) if f.lower().endswith((".mp3", ".wav"))]
    if not files:
        speak("No song found")
        print("No music files found in", music_dir)
        return
    if song_name:
        matches = [f for f in files if song_name.lower() in f.lower()]
        choice = matches[0] if matches else random.choice(files)
    else:
        choice = random.choice(files)
    path = os.path.join(music_dir, choice)
    speak("Playing music")
    print("Playing:", path)
    try:
        os.startfile(path)
    except Exception as e:
        print("Could not play file:", e)


def set_name() -> None:
    name = input("Enter new assistant name: ").strip()
    if name:
        with open("assistant_name.txt", "w", encoding="utf-8") as f:
            f.write(name)
        speak(f"Okay, I will be known as {name} from now on.")


def load_name() -> str:
    try:
        with open("assistant_name.txt", "r", encoding="utf-8") as f:
            return f.read().strip() or "Jarvis"
    except FileNotFoundError:
        return "Jarvis"


def search_wikipedia(query):
    if not query:
        speak("Please tell me what to search on Wikipedia.")
        return
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(summary)
        print(summary)
    except Exception as e:
        print("Wikipedia error:", e)
        speak("Sorry, I could not find results on Wikipedia.")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if any(g in query for g in ("hello", "hi", "hey")):
            speak("Hello sir. How can I help you?")
            print("Hello sir. How can I help you?")
            continue

        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            q = query.replace("wikipedia", "").strip()
            search_wikipedia(q)
        elif "play music" in query or "play" in query:
            name = query.replace("play music", "").replace("play", "").strip()
            play_music(name or None)
        elif "open youtube" in query:
            wb.open("https://youtube.com")
        elif "open google" in query:
            wb.open("https://google.com")
        elif "change your name" in query:
            set_name()
        elif "screenshot" in query:
            screenshot()
            speak("I've taken a screenshot.")
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break
        elif "help" in query:
            help_text = ("You can say: time, date, wikipedia <topic>, play music, open youtube, "
                         "open google, screenshot, tell me a joke, change your name, exit")
            speak(help_text)
            print(help_text)
        else:
            speak("I did not understand that. Please try again or type help for commands.")
            print(f"Unrecognized command: {query}. Type 'help' for a list of commands.")
