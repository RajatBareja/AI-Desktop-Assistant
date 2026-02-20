import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
import os
import time
import google.generativeai as genai
import music_library 

# ---------------- Gemini AI Setup ----------------
API_KEY = "AIzaSyAa5xZeTHZ7MyLRVQRdh_p_HEdxemigmX4" 
genai.configure(api_key=API_KEY)

def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Full paths are safer (models/gemini-1.5-flash)
        if 'models/gemini-1.5-flash' in available_models:
            return genai.GenerativeModel('models/gemini-1.5-flash')
        elif 'models/gemini-pro' in available_models:
            return genai.GenerativeModel('models/gemini-pro')
        else:
            return genai.GenerativeModel(available_models[0])
    except:
        return None

model = get_working_model()

# ---------------- TTS setup ----------------
engine = pyttsx3.init()
def speak(text):
    try:
        engine.say(text.split('.')[0]) 
        engine.runAndWait()
    except: pass

# ---------------- Nova App ----------------
class NovaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nova AI")
        self.root.geometry("900x750")
        self.root.configure(bg="white")
        
        self.attached_files = {} 
        self.thumbnails = [] 
        self.placeholder = "Ask Nova..."

        # Chat Area
        self.chat_display = tk.Text(root, bg="white", bd=0, font=("Segoe UI", 11), state="disabled", wrap="word")
        self.chat_display.pack(fill="both", expand=True, padx=25, pady=20)

        # Bottom UI
        self.bottom_wrapper = tk.Frame(root, bg="white")
        self.bottom_wrapper.pack(side="bottom", pady=20)

        self.search_container = tk.Frame(self.bottom_wrapper, bg="#f1f3f4", highlightbackground="#dfe1e5", highlightthickness=1)
        self.search_container.pack()

        self.attachment_bar = tk.Frame(self.search_container, bg="#f1f3f4")
        self.attachment_bar.pack(fill="x", padx=10, pady=(5, 0))

        self.input_row = tk.Frame(self.search_container, bg="#f1f3f4")
        self.input_row.pack(fill="x")

        self.plus_btn = tk.Button(self.input_row, text="+", font=("Arial", 18), bg="#f1f3f4", bd=0, command=self.add_attachment)
        self.plus_btn.pack(side="left", padx=(10, 5))

        self.entry = tk.Entry(self.input_row, font=("Segoe UI", 12), bg="#f1f3f4", bd=0, width=35, fg="black")
        self.entry.insert(0, self.placeholder)
        self.entry.pack(side="left", padx=5, ipady=10)
        
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<Return>", lambda e: self.handle_action())

        self.mic_btn = tk.Button(self.input_row, text="🎤", font=("Arial", 14), bg="#f1f3f4", bd=0, command=self.start_listening)
        self.mic_btn.pack(side="right", padx=10)

    def on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)

    def on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)

    def show_msg(self, sender, msg):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{sender}: {msg}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def set_reminder(self, task, seconds):
        def timer():
            time.sleep(seconds)
            messagebox.showinfo("Nova Reminder", f"Bhai, Time out! Task: {task}")
            speak(f"Reminder for {task}")
        threading.Thread(target=timer, daemon=True).start()

    def process_command(self, c):
        c = c.lower().strip()
        if not c or c == self.placeholder.lower(): return
        
        # 1. System Commands (Google/YT/Music)
        if "open google" in c:
            webbrowser.open("https://google.com")
            self.show_msg("Nova", "Opening Google...")
            return
        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")
            self.show_msg("Nova", "Opening YouTube...")
            return
        elif c.startswith("play"):
            try:
                song = c.split(" ", 1)[1]
                webbrowser.open(music_library.music[song])
                self.show_msg("Nova", f"Playing {song}...")
            except: self.show_msg("Nova", "Song not found.")
            return

        # 2. Reminder Check
        if "remind" in c or "reminder" in c:
            try:
                words = c.split()
                delay = 5
                for word in words:
                    if word.isdigit(): delay = int(word)
                if "min" in c: delay *= 60
                task = c.split("to")[-1] if "to" in c else "Task"
                self.show_msg("Nova", f"Theek hai bhai, {delay} seconds mein yaad dila dunga.")
                self.set_reminder(task, delay)
                return
            except: pass

        # 3. Default: Send to Gemini
        self.show_msg("You", c)
        img_list = list(self.attached_files.keys())
        threading.Thread(target=self.call_gemini, args=(c, img_list), daemon=True).start()

    def call_gemini(self, prompt, image_paths):
        if not model:
            self.show_msg("System", "Bhai API model load nahi hua. Key check kar.")
            return
        try:
            content = []
            if prompt: content.append(prompt)
            for path in image_paths:
                img = Image.open(path)
                content.append(img)
            
            if not content: content = ["Hello"]

            response = model.generate_content(content)
            res_text = response.text
            self.show_msg("Nova", res_text)
            threading.Thread(target=speak, args=(res_text,), daemon=True).start()
        except Exception as e:
            self.show_msg("System", f"Gemini Error: {e}")

    def handle_action(self):
        query = self.entry.get()
        # Important: Store files before clearing UI
        current_files = list(self.attached_files.keys())
        
        self.process_command(query)
        
        # Clear UI components
        for widget in self.attached_files.values():
            widget.destroy()
        self.attached_files = {}
        self.entry.delete(0, tk.END)
        self.on_focus_out(None)

    def add_attachment(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
        for path in files:
            if path in self.attached_files: continue
            tile = tk.Frame(self.attachment_bar, bg="#e8f0fe", highlightthickness=1)
            tile.pack(side="left", padx=3, pady=5)
            img = Image.open(path)
            img.thumbnail((35, 35))
            img_tk = ImageTk.PhotoImage(img)
            self.thumbnails.append(img_tk)
            tk.Label(tile, image=img_tk, bg="#e8f0fe").pack(side="left", padx=3, pady=3)
            tk.Button(tile, text="×", bg="#e8f0fe", bd=0, fg="red", command=lambda p=path, t=tile: self.remove_tile(p, t)).pack(side="right")
            self.attached_files[path] = tile

    def remove_tile(self, path, tile):
        tile.destroy()
        if path in self.attached_files:
            del self.attached_files[path]

    def start_listening(self):
        def listen():
            r = sr.Recognizer()
            with sr.Microphone() as s:
                r.adjust_for_ambient_noise(s)
                try:
                    audio = r.listen(s, timeout=5)
                    text = r.recognize_google(audio)
                    self.root.after(0, lambda: self.update_entry_and_process(text))
                except: pass
        threading.Thread(target=listen, daemon=True).start()

    def update_entry_and_process(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.process_command(text)

if __name__ == "__main__":
    root = tk.Tk()
    app = NovaApp(root)
    root.mainloop()