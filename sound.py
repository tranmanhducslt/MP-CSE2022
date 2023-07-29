import speech_recognition as sr
recognized_text = None
def recognize_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the source
    with sr.Microphone() as source:
        print("Calibrating ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration = 2)

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

if _name_ == "_main_":
    recognize_speech()