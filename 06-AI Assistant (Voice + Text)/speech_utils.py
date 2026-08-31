# speech_utils.py
import os
import threading

# Speech recognition and TTS libraries
import speech_recognition as sr
import pyttsx3

# Initialize TTS engine globally to avoid re-init delays
_tts_engine = None

def get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = pyttsx3.init()
        # Optional: set voice properties
        _tts_engine.setProperty('rate', 160)    # words per minute
        _tts_engine.setProperty('volume', 1.0)
    return _tts_engine

def speak_text(text, non_blocking=True):
    """Speak text using pyttsx3. By default runs in background thread."""
    def _speak():
        engine = get_tts_engine()
        engine.say(text)
        engine.runAndWait()
    if non_blocking:
        t = threading.Thread(target=_speak, daemon=True)
        t.start()
    else:
        _speak()

def listen_from_mic(timeout=5, phrase_time_limit=10):
    """Record audio from the default microphone and return recognized text (or None)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening (please speak)...")
        r.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return None
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None
