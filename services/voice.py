import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)


def speak(text):

    engine.say(text)

    engine.runAndWait()


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        return text

    except:

        return ""