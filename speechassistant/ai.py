import asyncio
import subprocess
import webbrowser
import speech_recognition as sr
import aiohttp
import edge_tts
import pywhatkit
import pyautogui
import datetime
import time

morse = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
    "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---",
    "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-",
    "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--",
    "z": "--.."
}

recognizer = sr.Recognizer()
mic = sr.Microphone()

async def play_audio(file):
    proc = await asyncio.create_subprocess_exec(
        "ffplay", "-nodisp", "-autoexit", file,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        await asyncio.wait_for(proc.wait(), timeout=10) 
    except asyncio.TimeoutError:
        proc.terminate() 

async def speak(text, voice="en-US-GuyNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save("response.mp3")
    await play_audio("response.mp3")

async def get_weather():
    url = "https://www.meteosource.com/api/v1/free/point"
    params = {
        "lat": 51.9625,
        "lon": 7.6256,
        "sections": "current",
        "language": "en",
        "units": "metric",
        "key": "6123qnjpyakv9nli6iabv2z7l995bsgtye007rz6"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            current = data.get("current", {})
            temp = current.get("temperature", "?")
            desc = current.get("summary", "No description")
            return temp, desc

async def get_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "eur"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data["bitcoin"]["eur"]

async def open_spotify():
    proc = await asyncio.create_subprocess_exec("spotify")
    await proc.wait()

async def open_youtube_channel():
    webbrowser.open("https://www.youtube.com/@NoTextToSpeech")

async def open_discord():
    proc = await asyncio.create_subprocess_exec("flatpak", "run", "com.discordapp.Discord")
    await proc.wait()




async def whatsapp():
    await asyncio.to_thread(
        pywhatkit.sendwhatmsg_instantly,
        "+nummber ...",
        "skibidi toilet ohio sigma",
        7  
    )
    pyautogui.click(x=1875, y=1037)



async def main():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    await speak("Hello I am ready and waiting for your command.")

    while True:
        with mic as source:
            print("Waiting for the hotword...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="en-US").lower()
            print("You:", text)

            if "jarvis" in text:
                command = text.replace("jarvis", "").strip()
                print("Command:", command)

                if "spotify" in command:
                    asyncio.create_task(open_spotify())
                    await speak("Opening Spotify.")
                elif "youtube" in command:
                    asyncio.create_task(open_youtube_channel())
                    await speak("Opening the YouTube channel No Text To Speech.")
                elif "discord" in command:
                    asyncio.create_task(open_discord())
                    await speak("Opening Discord.")
                elif "whatsapp" in command:
                    await whatsapp()
                elif "how are you" in command:
                    await speak("I am good. I cannot be sad or anything else than good because I am a machine, not a person.")
                elif "weather" in command:
                    temp, desc = await get_weather()
                    if temp is not None:
                        await speak(f"The weather in Münster is {desc} with a temperature of {temp} degrees Celsius.")
                    else:
                        await speak("I could not retrieve the weather data.")
                elif "morse" in command:
                    await speak("Which word do you want to convert to Morse code? Please type it in the console.")
                    word = input("Word for morse code: ").lower()
                    output = " ".join(morse.get(b, "") for b in word)
                    print("Morse code:", output)
                    await speak(f"The Morse code for {word} is {output}")
                elif "bitcoin" in command:
                    price = await get_bitcoin()
                    if price is not None:
                        await speak(f"The current Bitcoin price is {price} euros.")
                    else:
                        await speak("I could not retrieve the Bitcoin price.")
                elif any(word in command for word in ["bye", "exit", "goodbye"]):
                    await speak("Goodbye, see you soon!")
                    break
                else:
                    await speak("I did not understand the command.")
            else:
                print("Hotword not detected - ignoring.")

        except sr.UnknownValueError:
            print("I did not understand anything.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
