import speech_recognition as sr 
import playsound # to play saved mp3 file
import sounddevice as sd


def getAudio():
        #create a speech recognizer object
        rObject = sr.Recognizer()
        audio =""
        with sr.Microphone() as source:
                print("Start Speaking...")
                # recording the audio using speech recognition ,wait for 5 secs
                audio = rObject.listen(source,phrase_time_limit=5)
                print("Stop.") # limit 5 sec
        try:
                #convert speech to text
                text = rObject.recognize_google(audio, language ='en-US')
                print("You : ", text)
                return str(text)
        except:
                speak("Pardon me!!I couldn't understand you.Please repeat")
                return "bad input"
        

getAudio()  # Uncomment to test the getAudio function