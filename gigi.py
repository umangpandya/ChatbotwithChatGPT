import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import openai

openai.api_key="" #Add your open ai key here.



# Set up speech recognition
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    
    # r.pause_threshold = 1
    r.adjust_for_ambient_noise(source, duration = 1)
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
    except:
        print("sorry, could not recognise")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up wake-up keyword
wake_word = "Hello"

# Define function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define function for opening a website
def open_website(url):
    # Windows
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)
    speak("Opening website.")

# Define function for telling the time
def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}.")



def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# Check if wake-up keyword is detected
if wake_word in r.recognize_google(audio):
    speak("Yes Umang Sir?, How Can I help You?")
    
    # Listen for command
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)
    
    try:
        # Convert speech to text
        command = r.recognize_google(audio)
        print("You said: " + command)
        
        # Execute command
        

        if "open" in command:
            if "website" in command:
                url = command.split()[-1]
                open_website(url)
            else:
                speak("I'm not sure what you want me to open.")
        elif "time" in command:
            tell_time()
        
        else:
            prompt = f"""Your task is to answer the question as a assistant.
             Once your answer complete ask for further help on same topic.
             Use at most 50 words.
             Question provided in the question_command delimited by triple backticks.
             question_command: ```{command}```
             """
            response = get_completion(prompt)
            speak(response)

    except sr.UnknownValueError:
        speak("I'm sorry, I didn't understand that.")
    except sr.RequestError as e:
        speak("Sorry, I couldn't reach the Google servers. Check your internet connection.")