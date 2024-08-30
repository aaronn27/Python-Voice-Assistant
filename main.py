import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import requests
from googlesearch import search

# Initialize the recognizer
listener = sr.Recognizer()
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice property
voices = engine.getProperty('voices')

# Set the voice to male
# engine.setProperty('voice', voices[0].id)

# Set the voice to female
engine.setProperty('voice', voices[1].id)

#API Key for Weather
apikey = 'd5b049c1afcfece640ebdecaa8a4c608'

def talk(text):
    """
    Convert text to speech and speak it.
    """
    engine.say(text)
    engine.runAndWait()


def take_command():
    """
    Listen for a command from the user and return it as a string.
    """
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()

        if 'hey luna' in command or 'ok luna' in command or 'luna' in command:
            command = command.replace('luna', '')
            talk(command)
    return command

def get_weather(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" + apikey
    json_data = requests.get(api).json()

    if json_data["cod"] != "404":
        condition = json_data['weather'][0]['main']
        curr_temp = int(json_data['main']['temp'] - 273.15)
        talk(f"The weather in {city} is {condition} and the current temperature is {curr_temp} degree celsius.")
    else:
        talk("City Not Found")
        print("City Not Found")

def run_luna():
    """
    Process the command and execute corresponding actions.
    """
    command = take_command()
    print(command)

    # Play a song or open a YouTube video
    if 'play' in command:
        song = command.replace('play', '').replace('youtube', '')
        talk(f'Playing {song} in Youtube')
        pywhatkit.playonyt(song)

    # Tell the current time
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk(f'The Current time is {time}')

    # Tell the current date
    elif 'date' in command or 'today' in command:
        date = datetime.datetime.now().strftime('%d %B %Y')
        print(date)
        talk(f'Today is {date}')

    # Provide information about a person from Wikipedia
    elif 'who is' in command or 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    # Open Google in the web browser
    elif 'open google' in command:
        talk("Opening Google\n")
        webbrowser.open("google.com")

    # Open YouTube in the web browser
    elif 'open youtube' in command:
        talk("Opening Youtube\n")
        webbrowser.open("youtube.com")

    # Perform a Google Search
    elif 'what is' in command or 'google' in command:
        link = command.replace('what is', '').replace('google', '')
        talk("Here are some results\n")
        results = search(link, num_results=3)
        for result in results:
            print(result)

    # Tell a Joke
    elif 'joke' in command:
        jokes = talk(pyjokes.get_joke())
        print(jokes)
        talk(jokes)

    # Tell Weather updates
    elif 'weather' in command:
        print("Please say the city name:")
        talk("Please say the city name")
        city = take_command()
        get_weather(city)


    # Respond to Thank you
    elif 'thank you' in command:
        talk("I am glad that I could help you.")

    # Handle unrecognized commands
    else:
        talk('I’m sorry, I didn’t understand the command. Could you please repeat it?')


# Continuously run the voice assistant
while True:
    run_luna()
