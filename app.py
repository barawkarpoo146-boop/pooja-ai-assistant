import streamlit as st
from ai_engine import get_ai_response
import speech_recognition as sr
import pyttsx3
import time
import threading

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return ""

def set_reminder(message, seconds):
    def reminder():
        time.sleep(seconds)
        speak(f"Pooja! Reminder — {message}")
    thread = threading.Thread(target=reminder)
    thread.start()

st.title("🤖 Pooja AI Personal Assistant")
st.write("Hello Pooja! 😊")

st.sidebar.title("⏰ Set Reminder")
reminder_text = st.sidebar.text_input("Reminder:")
reminder_time = st.sidebar.number_input("Minutes after:", min_value=1, max_value=60)
if st.sidebar.button("Set Reminder ⏰"):
    set_reminder(reminder_text, reminder_time * 60)
    st.sidebar.success(f"✅ Reminder set for {reminder_time} minutes!")
    speak(f"Okay Pooja! I will remind you about {reminder_text} after {reminder_time} minutes!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if st.button("🎤 Speak to Pooja AI"):
    user_input = listen()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = get_ai_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        speak(response)
        st.rerun()

user_input = st.chat_input("Type here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_ai_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    speak(response)
    st.rerun()