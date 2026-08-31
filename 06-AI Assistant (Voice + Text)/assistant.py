# assistant.py
import os
import time
from speech_utils import listen_from_mic, speak_text
import argparse

# Optional dependency: OpenAI (only used if OPENAI_API_KEY is present)
USE_OPENAI = False
try:
    import openai
    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        USE_OPENAI = True
except Exception:
    USE_OPENAI = False

def get_reply_openai(prompt, model="gpt-4o-mini", max_tokens=150):
    """
    Calls OpenAI ChatCompletion or completions (adapt if API differs).
    This function attempts ChatCompletion-like call but checks availability.
    Note: If you plan to use OpenAI, set OPENAI_API_KEY env var first.
    """
    try:
        # simple completion-style call that works across common SDKs
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=0.6
        )
        # extract text
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI request failed:", e)
        return None

def get_reply_fallback(prompt):
    """Simple rule-based fallback for offline demo."""
    p = prompt.lower()
    if any(x in p for x in ["hello","hi","assalamu","hey"]):
        return "Hello — I am your assistant. How can I help you today?"
    if "time" in p:
        return f"The current time is {time.strftime('%H:%M:%S')}."
    if "your name" in p or "who are you" in p:
        return "I'm a demo AI Assistant built in Python. You can change me on GitHub."
    return "I don't have a smart answer offline. Try enabling OpenAI (set OPENAI_API_KEY) for better replies."

def chat_loop(voice=False, speak=False):
    print("Starting assistant. Type 'exit' to quit. Type 'voice' to use microphone if voice mode is enabled.")
    while True:
        if voice:
            text = listen_from_mic()
            if text is None:
                continue
            print("You said:", text)
        else:
            text = input("You: ").strip()
        if not text:
            continue
        if text.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        # Decide whether to use OpenAI
        reply = None
        if USE_OPENAI:
            reply = get_reply_openai(text)
        if not reply:
            reply = get_reply_fallback(text)

        print("Assistant:", reply)
        if speak:
            speak_text(reply)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", action="store_true", help="Enable voice input (microphone)")
    parser.add_argument("--speak", action="store_true", help="Enable text-to-speech output")
    args = parser.parse_args()
    chat_loop(voice=args.voice, speak=args.speak)
