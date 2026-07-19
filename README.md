# Nova AI — Desktop Voice & Chat Assistant

A Python desktop assistant built with `tkinter`, using Google's **Gemini API** for chat/vision responses, `speech_recognition` for voice input, and `pyttsx3` for text-to-speech. Supports typed or spoken commands, image attachments, reminders, and quick shortcuts (Google, YouTube, music).

## Features

- 🎤 **Voice input** — speak a command via microphone (Google Speech Recognition)
- 🔊 **Text-to-speech replies** — Nova speaks its responses back
- 🖼️ **Image attachments** — attach images and ask Gemini questions about them
- ⏰ **Reminders** — "remind me to X in 5 min" style commands
- 🎵 **Quick music shortcuts** — `play <song>` opens a YouTube link from `music_library.py`
- 🌐 **Quick shortcuts** — "open google", "open youtube"
- 💬 **Gemini-powered chat** — anything else is sent to the Gemini model

## Project Structure

```
.
├── nova.py              # Main app (GUI + logic)
├── jarvisgui_.py         # Earlier/simpler GUI prototype
├── music_library.py     # Song name → YouTube link mapping
├── import_google.py     # Helper script to list available Gemini models
├── requirements.txt     # Python dependencies
├── .env.example          # Template for your API key (copy to .env)
├── .gitignore            # Keeps .env and other junk out of git
└── README.md
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `pyaudio` can be tricky to install on Windows. If it fails, try:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 2. Add your Gemini API key

Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then open `.env` and paste your key:

```
GEMINI_API_KEY=your_actual_key_here
```

**Never commit `.env` to GitHub** — it's already excluded via `.gitignore`.

### 3. Run

```bash
python nova.py
```

## Checking available Gemini models

If you get a "model not found" error, run:

```bash
python import_google.py
```

This lists every model your API key currently has access to — use one of those names in `nova.py` if the default (`gemini-1.5-flash`) isn't available for your key.



## License

Personal project — use, modify, and share freely.
