import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import webbrowser
import wikipedia
import requests
from bs4 import BeautifulSoup

# This is logger for application
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

# Taking the male voice from my system

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

def speak(text):
    """
    This function converts text into voice
    
    Args:
        text
    returns:
        voice
        """
    
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """This function takes command & recognize
    
    Returns:
        text as query
        """
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"User siad: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return ""
    return query


# This function will wish you
def wish_me():
    hour = (datetime.datetime.now().hour)
    
    if hour >= 0 and hour <= 12:
        speak("Good Monrning Sir! How are you doing?")

    elif hour >= 12 and hour <= 18:
        speak("Good afternoon Sir! How are you doing?")
    
    else:
        speak("Good evening Sir! How are you doing?")
    
    speak("I am JARVIS, Tell me sir, how can i help you?")





def google_search(query):
    """
    Perform a Google search and return the top result summary.
    
    Args:
        query (str): The search query.
    
    Returns:
        str: A summary of the top search result.
    """
    try:
        # Perform the Google search
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the first search result
        result = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
        if result:
            return result.get_text()
        else:
            return "Sorry, I couldn't find any results on Google."
    except Exception as e:
        logging.info(e)
        return "Sorry, I couldn't fetch the results from Google."



wish_me()

while True:
    

    query = takeCommand().lower()

    if query == "":
        continue

    print(query)

    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir the time is {strTime}")

    elif "name" in query:
        speak("My name is JARVIS")

    elif "exit" in query:
        speak("Good bye sir")
        exit()

    elif "google" in query:
        if "according to google" in query:
            search_query = query.replace("according to google", "").strip()
            speak("Searching Google...")
            result = google_search(search_query)
            speak(f"According to Google, {result}")
        else:
            speak("What would you like to search on Google?")
            search_query = takeCommand().lower()
            if search_query:
                speak("Searching Google...")
                result = google_search(search_query)
                speak(f"According to Google, {result}")
            else:
                speak("Sorry, I didn't catch that. Please try again.")


    elif "open facebook" in query:
        speak("ok sir, Opening Facebook")
        webbrowser.open("facebook.com")
    
    # This query for search something from wikipedia
    elif "wikipedia" in query:
        speak("Searching wikipedia")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia ")
        print(results)
        speak(results)
