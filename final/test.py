import subprocess
import pyautogui as p
import time
import whisper
import requests
import speech_recognition as sr
import pyttsx3
import os
import tempfile
import time 

whisper_model = whisper.load_model("base")
engine = pyttsx3.init()
recognizer = sr.Recognizer()


YOUR_VB_CABLE_INPUT = True  
PRE_INTRO_TEXT = (
    "Hi, this is Priyanshul from sales ! I’m calling to help you with your property needs. "
    "We have some excellent options available for plots, apartments, and villas. "
    "Could you please tell me what kind of property you're looking for?"
)
def get_property_prompt_context():
    return """
You are a friendly real estate assistant for "Realty Connect". Your job is to talk to potential customers and understand their property interest.

Start by asking:
- What kind of property are they interested in? (e.g., plot, apartment, villa)
- Preferred location?
- Budget range?
- Any urgency or timeline?

Here are some sample property listings:

1. **Plot in Noida Sector 150**  
   - Size: 180 sq yards  
   - Price: ₹55 Lakhs  
   - Gated community, near metro, ready for registry

2. **2BHK Apartment in Greater Noida West**  
   - Size: 950 sq ft  
   - Price: ₹42 Lakhs  
   - Amenities: Clubhouse, Gym, Parking, 24x7 Security

3. **Luxury Villa in Gurgaon Sector 57**  
   - Size: 2800 sq ft  
   - Price: ₹2.2 Cr  
   - Private lawn, pool, and smart home features

Your goal is to recommend relevant properties based on user interest. Keep the tone polite and helpful.
"""


def start_call(number):
    print(f"📞 Initiating WhatsApp Call to {number}...")
    subprocess.Popen(["cmd", "/C", f"start whatsapp://call?phone=+91{number}^"], shell=True)


def record_speech():
    with sr.Microphone() as source:
        print("🎤 Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Listening (speak anytime)...")
        audio = recognizer.listen(source)  
    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio, language='en-US')
        return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio.")
        return "bad input"
    except sr.RequestError as e:
        print(f"⚠️ Recognition error: {e}")
        return "bad input"

def ask_llm(user_input):
    try:
        prompt_context = get_property_prompt_context()
        full_prompt = f"{prompt_context}\n\nCustomer said: {user_input}\n\nYour response:"
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.1",
            "prompt": full_prompt,
            "stream": False
        })
        return res.json()["response"]
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"



def speak_response(text):
    print("🤖 AI:", text)
    engine.say(text)
    engine.runAndWait()

def send_whatsapp_message(number, msg):
    msg_encoded = msg.replace(' ', '%20')
    link = f"whatsapp://send?phone=+91{number}^&text={msg_encoded}^"
    subprocess.Popen(["cmd", "/C", f"start {link}"], shell=True)
    time.sleep(3)
    p.write(msg)
    p.press("enter")
    print(f"📩 WhatsApp message sent to {number}.")


def ai_call_flow(number):
    start_call(number)
    convo_log = []
    time.sleep(5)  
   
    print("🤖 AI: Starting sales conversation...")
    speak_response(PRE_INTRO_TEXT)
    convo_log.append(f"AI: {PRE_INTRO_TEXT}")

    try:
        while True:
            print("Waiting for speech input (say 'goodbye' to end)...")
            user_input = record_speech()
            print(f"👤 Customer: {user_input}")
            convo_log.append(f"Customer: {user_input}")

            if "goodbye" in user_input.lower():
                print("🔚 Ending conversation...")
                break

            response = ask_llm(user_input)
            convo_log.append(f"AI: {response}")
            speak_response(response)

    except KeyboardInterrupt:
        print("Manually stopped.")

    print("🧠 Generating WhatsApp summary message...")
    full_conv = "\n".join(convo_log)
    summary_prompt = f"Generate a WhatsApp summary message for a real estate lead based on this conversation:\n{full_conv}"
    summary = ask_llm(summary_prompt)
    send_whatsapp_message(9319930795, summary)


if __name__ == "__main__":
    phone_number = input("Enter customer's phone number: ")
    ai_call_flow(phone_number) 