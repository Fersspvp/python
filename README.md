# Jarvis and Discord Bot

Hi there,  
this repository contains two Python projects I’ve been building:  
a speech assistant called **Jarvis**, and a **Discord bot** with moderation, music, and utility features.  

They’re separate, but both are built to be practical and fun.  
Jarvis handles voice commands and tasks on your computer,  
while the Discord bot manages and enhances Discord servers.

---

## Jarvis – The Speech Assistant

Jarvis is a small voice assistant that listens through your microphone, recognizes your speech, and responds using text-to-speech.  
It can open programs, check live data, and even chat a bit.

### What it can do
- Listens for a hotword (“Jarvis”)  
- Speaks back naturally using edge_tts  
- Gets the weather in Münster  
- Checks the Bitcoin price in real-time  
- Opens Spotify, YouTube, or Discord  
- Converts any word into Morse code  
- Sends WhatsApp messages  
- Says goodbye when you end the session  

### Example voice commands
- “Jarvis, open Spotify”  
- “Jarvis, what’s the weather?”  
- “Jarvis, convert hello to morse”  
- “Jarvis, what’s the Bitcoin price?”  
- “Jarvis, goodbye”

---

## Discord Bot

The Discord bot is designed for moderation, automation, and entertainment on servers like **Pixel.Network** and **Fritz.exe**.  
It supports both slash commands and prefix commands.

### Features
- Role-based moderation (ban, kick, etc.)  
- Bad word detection and filtering  
- Poll creation and reminders  
- Server information and custom embeds  
- Ticket system with buttons  
- Music playback from YouTube  
- Basic utility and fun commands  

### Example commands
- `/ban @user reason: spam`  
- `/kick @user reason: inactive`  
- `/reminder 10m Take a break`  
- `!play https://youtube.com/watch?v=...`  
- `/info_for_pixel-network`

---

## Tech Stack

**Python libraries used**
- discord.py  
- yt_dlp  
- aiohttp  
- speech_recognition  
- edge_tts  
- pywhatkit  
- pyautogui  

**Other tools**
- ffplay (for playing voice responses)  
- CoinGecko API (for Bitcoin price)  
- Meteosource API (for weather data)

---

## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/Fersspvp/python.git
   cd python
