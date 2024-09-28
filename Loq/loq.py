import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import requests
import json
import psutil
import subprocess
import pygame

engine = pyttsx3.init()

def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()

def time() -> None:
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)
    print("The current time is", Time)

def date() -> None:
    day: int = datetime.datetime.now().day
    month: int = datetime.datetime.now().month
    year: int = datetime.datetime.now().year
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)
    print(f"The current date is {day}/{month}/{year}")

def wishme() -> None:
    print("Welcome back sir!!")
    speak("Welcome back sir!!")

    hour: int = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good Morning Sir!!")
        print("Good Morning Sir!!")
    elif 12 <= hour < 16:
        speak("Good Afternoon Sir!!")
        print("Good Afternoon Sir!!")
    elif 16 <= hour < 24:
        speak("Good Evening Sir!!")
        print("Good Evening Sir!!")
    else:
        speak("Good Night Sir, See You Tomorrow")

    speak("LOQ at your service sir, please tell me how may I help you.")
    print("LOQ at your service sir, please tell me how may I help you.")

def screenshot() -> None:
    img = pyautogui.screenshot()
    img_path = os.path.expanduser(r"A:\Job\Voice Assistant (LOQ)\Loq\Images\screenshot.png")
    img.save(img_path)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)

    except Exception as e:
        print(e)
        speak("Please say that again")
        return "Try Again"

    return query

def weather():
    api_key = "b5f427ea5d4bf0267905223c8e09896e"  # Replace with your valid API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    speak("Please tell me the city name")
    city_name = takecommand().lower()
    
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") == 200:
        main = data["main"]
        temperature = main["temp"] - 273.15  # Kelvin to Celsius conversion
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        
        speak(f"The temperature in {city_name} is {temperature:.2f} degree Celsius.")
        speak(f"The weather is {weather_desc} with a humidity of {humidity} percent.")
        
        print(f"Temperature: {temperature:.2f}°C\nDescription: {weather_desc}\nHumidity: {humidity}%")
    else:
        error_message = data.get("message", "Something went wrong.")
        speak(f"Unable to find the city. {error_message}")
        print(f"City not found: {error_message}")

def news():
    news_api_key = "3ef65efa5318400a90865ff0de6a3087"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            if articles:
                speak("Here are the top headlines")
                for i, article in enumerate(articles[:3], start=1):
                    headline = article.get('title', 'No title available')
                    speak(f"Headline {i}: {headline}")
                    print(f"Headline {i}: {headline}")
            else:
                speak("No articles found.")
                print("No articles found.")
        else:
            speak("Failed to retrieve news.")
            print("Failed to retrieve news.")
    
    except requests.RequestException as e:
        speak("There was an error while fetching the news.")
        print("Error:", e)

def open_application(app_name):
    if "notepad" in app_name:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in app_name or "calc" in app_name:
        speak("Opening Calculator")
        os.system("start calc")
    else:
        speak(f"Sorry, I can't open {app_name} right now.")

def close_application(app_name):
    if "notepad" in app_name:
        speak("Closing Notepad")
        close_process("notepad.exe")
    elif "calculator" in app_name or "calc" in app_name:
        speak("Closing Calculator")
        close_process("calc.exe")
    else:
        speak(f"Sorry, I can't close {app_name} right now.")

def close_process(process_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == process_name.lower():
            proc.terminate()
            speak(f"{process_name} has been closed.")
            return
    speak(f"{process_name} not running.")

def system_command(command):
    if "shutdown" in command or "shut down" in command:
        speak("Shutting down the system.")
        try:
            subprocess.run(["shutdown", "/s", "/t", "1"], check=True)
        except subprocess.CalledProcessError as e:
            speak("Failed to execute shutdown command.")
            print(e)
    elif "restart" in command:
        speak("Restarting the system.")
        try:
            subprocess.run(["shutdown", "/r", "/t", "1"], check=True)
        except subprocess.CalledProcessError as e:
            speak("Failed to execute restart command.")
            print(e)
    else:
        speak("Sorry, I didn't understand the command.")

pygame.mixer.init()

def play_music():
    song_dir = os.path.expanduser(r"A:\Miscellaneous\Edits\Music for youtube")
    songs = os.listdir(song_dir)
    
    if len(songs) > 0:
        print(songs)
        x = len(songs)
        y = random.randint(0, x - 1)
        
        song_path = os.path.join(song_dir, songs[y])
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        print(f"Playing: {songs[y]}")
        speak(f"Playing {songs[y]}")
    else:
        speak("No songs found in the directory.")
        print("No songs found in the directory.")

def pause_music():
    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.pause()
        speak("Music paused.")
        print("Music paused.")
    else:
        speak("No music is playing right now.")
        print("No music is playing right now.")

def resume_music():
    if not pygame.mixer.music.get_busy():  # Check if music is paused
        pygame.mixer.music.unpause()
        speak("Music resumed.")
        print("Music resumed.")
    else:
        speak("No music is paused.")
        print("No music is paused.")

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "who are you" in query or "hu r u" in query:
            speak("I'm LOQ created by Mr. Rashmi Ranjan and I'm a desktop voice assistant.")
            print("I'm LOQ created by Mr. Rashmi Ranjan and I'm a desktop voice assistant.")

        elif "how are you"  in query or "how r u" in query:
            speak("I'm fine sir, What about you?")
            print("I'm fine sir, What about you?")

        elif "fine" in query or "good" in query:
            speak("Glad to hear that sir!!")
            print("Glad to hear that sir!!")

        elif "wikipedia" in query:
            try:
                speak("Ok wait sir, I'm searching...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except:
                speak("Can't find this page sir, please ask something else")

        elif "open youtube" in query:
            wb.open("youtube.com")

        elif "open google" in query:
            wb.open("google.com")

        elif "open stack overflow" in query:
            wb.open("stackoverflow.com")

        elif "play music" in query:
            play_music()

        elif "pause music" in query:
            pause_music()

        elif "resume music" in query:
            resume_music()
            
        elif "open brave" in query:
            bravePath = r"C:\Users\rrbis\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave.lnk"
            os.startfile(bravePath)

        elif "search on brave" in query:
            try:
                speak("What should I search?")
                print("What should I search?")
                search = takecommand()
                bravePath = r"C:\Users\rrbis\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
                search_url = f"https://www.google.com/search?q={search}"
                subprocess.Popen([bravePath, search_url])
                print(f"Searching for: {search}")

            except Exception as e:
                speak("Can't open now, please try again later.")
                print("Can't open now, please try again later.")
                print("Error:", e)
                
        elif "remember that" in query:
            speak("What should I remember")
            data = takecommand()
            speak("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))

        elif "screenshot" in query:
            screenshot()
            speak("I've taken a screenshot, please check it.")

        elif "weather" in query:
            weather()

        elif "news" in query:
            news()

        elif "open" in query:
            app_name = query.replace("open ", "")
            open_application(app_name)
        
        elif "close" in query:
            app_name = query.replace("close", "")
            close_application(app_name)

        elif "shutdown" in query or "shut down" in query or "restart" in query:
            system_command(query)

        elif "offline" in query:
            quit()
