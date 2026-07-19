import speech_recognition as sr
import pyttsx3
import threading
import tkinter as tk

# ===================== TTS =====================
engine = pyttsx3.init()
engine.setProperty("rate", 180)

def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

# ===================== SPEECH =====================
def listen():
    def _listen():
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                status.set("Listening...")
                audio = r.listen(source, timeout=5)

            text = r.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, text)
            status.set("Done")
            speak(text)

        except:
            status.set("Could not hear")

    threading.Thread(target=_listen, daemon=True).start()

# ===================== ROUNDED RECT =====================
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y1+r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# ===================== GUI =====================
root = tk.Tk()
root.title("Assistant")
root.geometry("900x600")
root.configure(bg="white")

# ---------- Status ----------
status = tk.StringVar(value="Ready")
tk.Label(
    root,
    textvariable=status,
    bg="white",
    fg="#666",
    font=("Segoe UI", 10)
).pack(side="bottom", pady=8)

# ---------- Bottom ----------
bottom = tk.Frame(root, bg="white")
bottom.pack(side="bottom", pady=25)

# ---------- Canvas Bar ----------
WIDTH = 520
HEIGHT = 44   # 👈 THIN height
RADIUS = 22   # 👈 cylindrical

canvas = tk.Canvas(
    bottom,
    width=WIDTH,
    height=HEIGHT,
    bg="white",
    highlightthickness=0
)
canvas.pack()

rounded_rect(
    canvas,
    2, 2,
    WIDTH-2, HEIGHT-2,
    RADIUS,
    fill="#f1f3f4",
    outline="#dadce0"
)

# ---------- + Button ----------
plus = tk.Button(
    canvas,
    text="+",
    font=("Segoe UI", 14),
    bg="#f1f3f4",
    bd=0,
    activebackground="#e8eaed"
)
canvas.create_window(25, HEIGHT//2, window=plus)

# ---------- Entry ----------
entry = tk.Entry(
    canvas,
    font=("Segoe UI", 13),
    bg="#f1f3f4",
    bd=0,
    width=34
)
canvas.create_window(WIDTH//2, HEIGHT//2, window=entry)

# ---------- Mic ----------
mic = tk.Button(
    canvas,
    text="🎤",
    font=("Segoe UI", 14),
    bg="#f1f3f4",
    bd=0,
    activebackground="#e8eaed",
    command=listen
)
canvas.create_window(WIDTH-30, HEIGHT//2, window=mic)

root.mainloop()
