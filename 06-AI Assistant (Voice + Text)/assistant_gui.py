# assistant_gui.py
import os
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from speech_utils import listen_from_mic, speak_text
from assistant import USE_OPENAI, get_reply_openai, get_reply_fallback

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant (Voice + Text)")
        self.chat_area = ScrolledText(root, state='disabled', width=70, height=20)
        self.chat_area.pack(padx=10, pady=8)
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=6)
        self.entry = tk.Entry(frame, width=50)
        self.entry.pack(side='left', padx=(0,6))
        self.send_btn = tk.Button(frame, text="Send", command=self.on_send)
        self.send_btn.pack(side='left')
        self.mic_btn = tk.Button(root, text="🎤 Speak", command=self.on_mic)
        self.mic_btn.pack(pady=(6,10))
        self.status = tk.Label(root, text="Ready")
        self.status.pack()
        root.bind('<Return>', lambda e: self.on_send())

    def append(self, text, tag=None):
        self.chat_area.configure(state='normal')
        self.chat_area.insert('end', text + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.see('end')

    def on_send(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, 'end')
        self.append("You: " + user_text)
        threading.Thread(target=self.get_and_display_reply, args=(user_text,), daemon=True).start()

    def on_mic(self):
        self.status.config(text="Listening...")
        threading.Thread(target=self._listen_and_process, daemon=True).start()

    def _listen_and_process(self):
        text = listen_from_mic()
        self.status.config(text="Processing...")
        if text:
            self.append("You (voice): " + text)
            self.get_and_display_reply(text)
        else:
            self.append("[Could not understand speech]")
        self.status.config(text="Ready")

    def get_and_display_reply(self, prompt):
        reply = None
        if USE_OPENAI:
            reply = get_reply_openai(prompt)
        if not reply:
            reply = get_reply_fallback(prompt)
        self.append("Assistant: " + reply)
        # speak the reply
        speak_text(reply)

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()
