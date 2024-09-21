import pyttsx3
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC  # Consider using a more advanced classifier for intent
import nltk
from sklearn.model_selection import train_test_split
import random
import warnings
import google.generativeai as genai
import datetime

warnings.simplefilter('ignore')

# nltk.download("punkt")  # Uncomment if needed

# Replace with your actual Gemini API key
GENENI_API_KEY = "AIzaSyAeUMBKGEbcxjT9DDS50BQk0otJsFayExo"  # Placeholder, replace with your key

# Configure Gemini API
genai.configure(api_key=GENENI_API_KEY)


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')  # Optional voice setting
    print(f"==> Friday AI: {text}")
    engine.say(text=text)
    engine.runAndWait()


def get_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, 0, 5)

    try:
        query = recognizer.recognize_google(audio, language="en").lower()
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Request failed: {e}")
        return None


def handle_user_intent(user_input):
    # Basic intent classification using keywords (can be extended with ML)
    if user_input in ["time", "today", "what is time"]:
        time = datetime.datetime.now().strftime('%H:%M:%S')
        today = datetime.date.today().strftime('%d %B, %Y')
        if user_input == "time":
            speak(f"Current time in India is {time}")
        else:
            speak(f"Today's date is {today}")
    elif user_input in ["exit", "goodbye"]:
        speak("Goodbye!")
        exit(0)
    else:
        # Use Gemini AI for complex queries
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(user_input, stream=True)
            for chunk in response:
                print(chunk.text)
                print("_" * 80)  # Separator between response chunks
            speak(response.text)
        except genai.GenerativeModelError as e:
            print(f"Error with Gemini AI: {e}")
            speak("Sorry, I encountered an issue. Please try again later.")


def main():
    speak("Hello Meet! My name is Friday, How can I assist you?")
    while True:
        user_input = get_user_input()
        if user_input:
            handle_user_intent(user_input)


if __name__ == "__main__":
    main()
