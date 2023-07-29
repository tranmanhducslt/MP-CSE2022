'''
Here's a step-to-step guide to get the voice recognition to work:

1. Install the SpeechRecognition library. You can do this using pip, the package manager for Python. Open your terminal or command prompt and run the following command:

pip install SpeechRecognition

2. To use SpeechRecognition, you'll need to have the necessary backend recognition engines installed. The library supports several engines like Google Web Speech API, CMU Sphinx, Microsoft Bing Voice Recognition, etc. One of the popular and easy-to-use choices is Google's Web Speech API.
To use the Google Web Speech API, you'll need to install the pyaudio library as well. You can install it with pip:

pip install pyaudio

After that, execute the code below and you're good to go!

'''
recognized_text = None
manual_activated = "Manual on"

import speech_recognition as sr

def recognize_speech(manual = False):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the source
    with sr.Microphone() as source:
        print("Calibrating ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print("Listening... Say something.")
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API to recognize the speech
        recognized_text = recognizer.recognize_google(audio)
        print("You said:", recognized_text.capitalize())
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print("Error occurred during the request to the Google Web Speech API:", e)

    return recognized_text
