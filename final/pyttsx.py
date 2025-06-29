import pyttsx3

engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')
for voice in voices:
    
    print(f"Voice ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender}")
engine.setProperty('rate', 150)  # Adjust speaking rate
engine.setProperty('volume', 0.9) # Adjust volume

engine.say("Hello, this is a personalized message.")
engine.runAndWait()