import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import random
import json
import requests
import wolframalpha

"""The main speaking engine is here"""
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.getProperty("rate")
engine.setProperty("rate", rate - 80)


def login(name):
    """General Login of the user"""
    with open("record.txt", "a") as f:
        f.write(f"{name} has started jarvis on {datetime.datetime.now()}\n")


def record_query(query, name):
    """Get the data for data analysis which is collected by this function"""
    with open("queries.txt", "a") as f:
        f.write(f"{query} : command by {name} on {datetime.datetime.now()}\n")


def Hello(name):
    """It is used in starting wish as well as ending wish..."""
    time = int(datetime.datetime.now().hour)
    if time >= 0 and time < 12:
        speak(f"Good Morning {name}")
    elif time >= 12 and time < 17:
        speak(f"Good Afternoon {name}")
    elif time >= 17 and time < 19:
        speak(f"Good Evening {name}")
    else:
        speak(f"Hey {name}, I think it's so dark outside..!")


def speak(audio):
    """It is used to speak the audio output"""
    engine.say(audio)
    engine.runAndWait()

def News_API(query):
    countrys = {'argentina': 'ar', 'australia': 'au', 'austria': 'at', 'belgium': 'be', 'brazil': 'br',
                'bulgaria': 'bg', 'canada': 'ca', 'china': 'cn', 'colombia': 'co',
                'cuba': 'cu', 'czech republic': 'cz', 'egypt': 'eg', 'france': 'fr', 'germany': 'de',
                'greece': 'gr',
                'hong kong': 'hk', 'iungary': 'hu', 'india': 'in',
                'indonesia': 'id', 'ireland': 'ie', 'israel': 'il', 'italy': 'it', 'japan': 'jp',
                'latvia': 'lv',
                'lithuania': 'it', 'malaysia': 'my', 'mexico': 'mx',
                'morocco': 'ma', 'netherlands': 'nl', 'new zealand': 'nz', 'nigeria': 'ng', 'norway': 'no',
                'philippines': 'ph', 'poland': 'pl', 'portugal': 'pt',
                'romania': 'ro', 'russia': 'ru', 'saudi arabia': 'sa', 'serbia': 'rs', 'singapore': 'sg',
                'slovakia': 'sk', 'slovenia': 'si', 'south africa': 'za',
                'south korea': 'kr', 'sweden': 'se', 'switzerland': 'ch', 'taiwan': 'tw', 'thailand': 'th',
                'turkey': 'tr', 'uae': 'ae', 'ukraine': 'ua',
                'united kingdom': 'gb', 'united states': 'us', 'venuzuela': 've'}
    loop(countrys)
    speak("From which country do you want to get news.")
    country = Take_Command(name).lower()  # This will give us the country
    # country = input("\nEnter the country:")  # This is useful when there is no internet connection
    for item in countrys.keys():
        if item in country:
            country1 = countrys.get(item)

            categories = ['business', 'entertainment', 'health', 'science', 'sports',
                          'technology']  # This will give us the category of news
            loop(categories)
            speak("Enter the category.")
            category = Take_Command(name).lower()
            # category = input("\nEnter the category:")  # This is useful when there is no internet connection
            for i in categories:
                if i in category:
                    url = (
                        f'https://newsapi.org/v2/top-headlines?country={country1.lower()}&category={i}&apiKey=2114b271bda54165b23a311b1d1e3c49')
                    try:
                        response = requests.get(url).text
                        news = json.loads(response)
                        print(news)
                        print(news["articles"])
                        articles = news["articles"]
                    except Exception as error:
                        print(f"This is the error: {error}")
                        print("\nSomething wents wrong...! Please try again...!")
                        speak("Sorry...! Something wents wrong...! Please try again...!")
                        continue
                    else:
                        if news["totalResults"] == 0:
                            print("Sorry, there is no news on this topic...!")
                            speak("Sorry, there is no news on this topic...!")
                            continue
                        number = news["totalResults"]
                        print(f"\nThere were {number} results found by API..!")
                        variable = 1
                        for article in articles:
                            print(variable)
                            print(article["title"])
                            speak(article["title"])
                            speak("The news description is ....!")
                            print(article["description"])
                            description = article["description"]
                            speak(description)
                            speak("The news content is ....!")
                            print(article["content"])
                            content = article["content"]
                            speak(content)
                            print(article["url"])  # This is for get the news directly from the link
                            if variable == 20:
                                speak("Thanks for listening us..!")
                                break
                            speak("The next news is.....!")
                            variable = variable + 1
                        break
                continue

def search(query):
    # try is used for searching with wolframAlpha
    try:
        # Generate your App ID from WolframAlpha
        app_id = "sachindabhdae1922@gmail.com"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        print(answer)
        speak("Your answer is " + answer)
    # If the query cannot be searched using WolframAlpha then it is searched wikipedia
    except:
        query = query.split(' ')
        query = " ".join(query[0:])
        speak("I am searching for " + query)
        print(wikipedia.summary(query, sentences=3))
        speak(wikipedia.summary(query, sentences=3))

def wiki(query):
    speak("Searching Wikipedia...!")
    query = query.strip().split(' ')
    query = " ".join(query[0:])
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("Alright, According to Wikipedia")
    print(results)
    speak(results)

def Take_Command(name):
    """It simply take command from the user"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 500
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"{name} said: {query}\n")
    except Exception as error:
        print(f"This is the error: {error}")
        print("Please speak clearly...")
        speak("Please speak clearly...")
        return "None"
    return query


def jarvis_info():
    for voice in voices:
        # to get the info. about various voices in our PC
        print("Voice:")
        print("ID: %s" % voice.id)
        print("Name: %s" % voice.name)
        print("Age: %s" % voice.age)
        print("Gender: %s" % voice.gender)
        print("Languages Known: %s" % voice.languages)


def loop(msg):
    """This is for creating loop to give the user options"""
    for i in msg:
        print(i, end=", ")


def SendEmail(toMail, content):
    """This is the function to send the emails directly from the programme"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("sachin1922dabhade1998@gmail.com", "dabhade@12")
    server.sendmail("sachin1922dabhade1998@gmail.com", toMail, content)
    server.close()


Software_list = {"open pycharm": "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.1.2\\bin\\pycharm64.exe",
                 "open visual studio": "C:\\Users\\VAIBHAV\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                 "open android studio": "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe",
                 "open chrome": "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                 "open python course": "D:\\Python Full Course with Projects"}

websites = {"open youtube": "youtube.com", "open google": "google.com", "open flipkart": "flipkart.com",
            "open amazon": "amazon.com", "open quora": "quora.com", "open facebook": "facebook.com",
            "open instagram": "instagram.com", "open stackoverflow": "stackoverflow.com", "open blog": "blogger.com",
            "open whatsapp": "web.whatsapp.com"}

talk_in_list = ['hii', 'hello', 'hello jarvis', 'jarvis', 'assistant', 'hey jarvis', 'hey dude']
talk_out_list = ['Always at your service sir', 'Order sir', 'Hello sir', 'what can i do for you sir', 'Yes sir',
                 'Beg for the order sir', 'How may i help you sir']

intro_temp = {'name': 'My name is jarvis.', 'work': 'My work is to help people as an assistant.',
              'who made you': 'I am made by Mr. Sachin Vinayak Dabhade,',
              'version': 'Kalank Version 1.1', 'speed': 'Transfer speed 500 mb per second',
              'favourite work': 'I like to help people.'}

if __name__ == '__main__':
    speak("What is your nane..!")  # This will get the name and use it in programme
    name = Take_Command("User").capitalize()
    # name = input("\nEnter the name:")  # This is useful when there is no internet connection
    login(name)
    Hello(name)
    print("This is your personal Artificial Intelligence, \"Kalank\" verson 1.1")
    speak("How may i help you..!")
    chance = 1
    while True:
        query = Take_Command(name).lower()  # This is the main query that user searches by voice
        # query = input("Enter the search:")  # This is the query when there were no internet on computer

        # This is the query recording function for getting know that what the user want from us
        record_query(query, name)

        # This is the main file for searching wikipedia on google
        if "wikipedia" in query:
            try:
                wiki(query)
            except Exception as e:
                print("The error is : {}".format(e))
            continue

        # Main file to give the news updates of all over the world
        elif "news" in query:
            News_API(query)
            continue

        # The main file to play music
        elif "play music" in query or "start music" in query or "music jarvis" in query:
            music_dir = "C:\\Users\\VAIBHAV\\Music\\Playlists"
            music = os.listdir(music_dir)
            print(music)
            i = random.randint(0, len(music) - 1)
            os.startfile(os.path.join(music_dir, music[i]))
            speak("playing music..!")
            continue

        # This will work like a google
        elif "search" in query or "what is meant by" in query:
            if "search" in query:
                query = query.replace("search", ' ')
                search(query)
            elif "what is meant by" in query:
                query = query.replace("what is meant by", ' ')
                search(query)
            continue

        # The main file to speak time
        elif "the time" in query:
            strtime = datetime.datetime.now().strftime("%H:%M")
            print(f"It's {strtime}")
            speak(f"It's {strtime}")
            continue

        # This is the main file of sending emal to the other person
        elif "send email" in query:
            EmailList = {"sachin": "sachin1922dabhade1998@gmail.com", "vaibhav": "vaibhavdabhade97@gmail.com"}
            try:
                speak("To whom do you want to send email")
                to = Take_Command(name).lower()
                speak("What do you want to send...!")
                content = Take_Command(name).capitalize()
                toMail = EmailList.get(to)
                SendEmail(toMail, content)
                speak("Email sent..!")
            except Exception as e:
                print("Sorry, the email is not send:", e)
                speak("Sorry, the email is not send.")
            continue

        # This is the main file for quiting the programme
        elif "sleep jarvis" in query or "quit" in query or "by jarvis" in query:
            option = ["I think i have to sleep", "Sure sir", "Take care sir", "All right sir",
                      "Sleeping artificial intelligence", "Have a nice day sir"]
            random_quit = random.randint(0, len(option) - 1)
            print(option[random_quit])
            speak(option[random_quit])
            exit()

        # This are the for loops useful for specific command in jarvis
        else:
            # This is the main file for the common responses of the user command
            for item in talk_in_list:
                if item in query:
                    number_random = random.randint(0, len(talk_out_list) - 1)
                    print(talk_out_list[number_random])
                    speak(talk_out_list[number_random])
                    break

                # This is the main file for giving the jarvis introduction
            for i in intro_temp.keys():
                if "jarvis voice" in query or "your voice" in query or "your information" in query:
                    jarvis_info()
                    speak("That's my information...!")
                elif "introduce yourself" in query or "your introduction" in query:
                    print(intro_temp.get(i))
                    speak(intro_temp.get(i))
                elif i in query:
                    speak(intro_temp.get(i))
                    break

                # Main file to perform the open application operations
            for i in Software_list:
                if i in query:
                    os.startfile(Software_list.get(i))
                    software = i.replace("open ", "")
                    speak(f"Opening {software}")
                    break

                # This is the website opening file
            for i in websites.keys():
                if i in query:
                    webbrowser.open(websites.get(i))
                    web = i.replace("open ", "")
                    speak(f"Opening {web}")
                    break

        chance = chance + 1
        continue
