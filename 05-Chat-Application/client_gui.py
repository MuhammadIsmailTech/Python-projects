# client_gui.py
import socket
import threading
import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import argparse

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

class ChatClient:
    def __init__(self, host, port, name, encrypted=False, key=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.fernet = None
        if encrypted:
            if not CRYPTO_AVAILABLE:
                raise RuntimeError("cryptography not installed")
            self.fernet = Fernet(key)
        self.name = name
        join_payload = json.dumps({"cmd":"join","name":name})
        if self.fernet:
            self.sock.sendall(self.fernet.encrypt(join_payload.encode()))
        else:
            self.sock.sendall(join_payload.encode())

        self.root = tk.Tk()
        self.root.title(f"Chat - {name}")
        self.chat_area = ScrolledText(self.root, state='disabled', width=60, height=20)
        self.chat_area.pack(padx=10, pady=10)
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(side='left', padx=10, pady=5)
        self.send_btn = tk.Button(self.root, text="Send", command=self.send_msg)
        self.send_btn.pack(side='left', padx=5)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        t = threading.Thread(target=self.recv_loop, daemon=True)
        t.start()
        self.root.mainloop()

    def add_text(self, text):
        self.chat_area.configure(state='normal')
        self.chat_area.insert('end', text + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.see('end')

    def recv_loop(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    self.add_text("[Disconnected from server]")
                    break
                if self.fernet:
                    data = self.fernet.decrypt(data).decode()
                else:
                    data = data.decode()
                self.add_text(data)
            except Exception as e:
                break

    def send_msg(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        out = msg.encode()
        if self.fernet:
            out = self.fernet.encrypt(out)
        try:
            self.sock.sendall(out)
            self.entry.delete(0, 'end')
        except Exception:
            self.add_text("[Failed to send message]")

    def on_close(self):
        try:
            out = "/quit".encode()
            if self.fernet:
                out = self.fernet.encrypt(out)
            self.sock.sendall(out)
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        self.root.destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--name", required=True)
    parser.add_argument("--encrypt", action="store_true")
    parser.add_argument("--key", type=str, help="Fernet key")
    args = parser.parse_args()
    key = args.key.encode() if args.key else None
    ChatClient(args.host, args.port, args.name, encrypted=args.encrypt, key=key)
