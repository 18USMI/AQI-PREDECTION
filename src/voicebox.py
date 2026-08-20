from gtts import gTTS
import pygame
import tkinter as tk
import os
import time

def speak(text):
    lang = language_var.get()   # get selected language
    
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove("voice.mp3")

# Create window
root = tk.Tk()
root.title("AI VoiceBox")

# 🔥 Full screen
root.attributes("-fullscreen", True)

# Dark background
root.configure(bg="#121212")

# Exit button (important!)
def exit_app():
    root.destroy()

tk.Button(root, text="❌ Exit", command=exit_app, bg="red", fg="white").pack(anchor="ne", padx=10, pady=10)

# Title
tk.Label(
    root, 
    text="AI VoiceBox", 
    font=("Arial", 30, "bold"), 
    fg="white", 
    bg="#121212"
).pack(pady=20)

# 🌍 Language Selection
language_var = tk.StringVar(value="en")

tk.Label(root, text="Select Language", fg="white", bg="#121212", font=("Arial", 14)).pack()

tk.OptionMenu(root, language_var, "en", "hi", "bn").pack(pady=10)

# Button style
btn_style = {
    "width": 30,
    "height": 2,
    "bg": "#1f1f1f",
    "fg": "white",
    "activebackground": "#333333",
    "activeforeground": "white",
    "bd": 0
}

# Buttons
tk.Button(root, text="Hello", command=lambda: speak("Hello"), **btn_style).pack(pady=10)
tk.Button(root, text="I need help", command=lambda: speak("I need help"), **btn_style).pack(pady=10)
tk.Button(root, text="Thank you", command=lambda: speak("Thank you"), **btn_style).pack(pady=10)

# Input
tk.Label(root, text="Type your message:", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 14), bg="#1f1f1f", fg="white", insertbackground="white")
entry.pack(pady=10)

tk.Button(root, text="Speak", command=lambda: speak(entry.get()), **btn_style).pack(pady=20)

# Run app
root.mainloop()



#another code which work

 
from gtts import gTTS
import pygame
import tkinter as tk
import os
import time

def speak(text):
    lang = language_var.get()   # get selected language
    
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove("voice.mp3")

# Create window
root = tk.Tk()
root.title("AI VoiceBox")

# 🔥 Full screen
root.attributes("-fullscreen", True)

# Dark background
root.configure(bg="#121212")

# Exit button (important!)
def exit_app():
    root.destroy()

tk.Button(root, text="❌ Exit", command=exit_app, bg="red", fg="white").pack(anchor="ne", padx=10, pady=10)

# Title
tk.Label(
    root, 
    text="AI VoiceBox", 
    font=("Arial", 30, "bold"), 
    fg="white", 
    bg="#121212"
).pack(pady=20)

# 🌍 Language Selection
language_var = tk.StringVar(value="en")

tk.Label(root, text="Select Language", fg="white", bg="#121212", font=("Arial", 14)).pack()

tk.OptionMenu(root, language_var, "en", "hi", "bn").pack(pady=10)

# Button style
btn_style = {
    "width": 30,
    "height": 2,
    "bg": "#1f1f1f",
    "fg": "white",
    "activebackground": "#333333",
    "activeforeground": "white",
    "bd": 0
}

# Buttons
tk.Button(root, text="Hello", command=lambda: speak("Hello"), **btn_style).pack(pady=10)
tk.Button(root, text="I need help", command=lambda: speak("I need help"), **btn_style).pack(pady=10)
tk.Button(root, text="Thank you", command=lambda: speak("Thank you"), **btn_style).pack(pady=10)

# Input
tk.Label(root, text="Type your message:", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 14), bg="#1f1f1f", fg="white", insertbackground="white")
entry.pack(pady=10)

tk.Button(root, text="Speak", command=lambda: speak(entry.get()), **btn_style).pack(pady=20)

# Run app
root.mainloop()





#another which gave hin,beng,eng

from gtts import gTTS
from googletrans import Translator
import pygame
import tkinter as tk
import os
import time

# Translator
translator = Translator()

def speak(text):
    lang = language_var.get()
    
    # Translate English → selected language
    translated = translator.translate(text, dest=lang).text
    
    tts = gTTS(text=translated, lang=lang)
    tts.save("voice.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
    os.remove("voice.mp3")

# Create window
root = tk.Tk()
root.title("AI VoiceBox")
root.attributes("-fullscreen", True)
root.configure(bg="#121212")

# Exit button
tk.Button(root, text="❌ Exit", command=root.destroy, bg="red", fg="white").pack(anchor="ne", padx=10, pady=10)

# Title
tk.Label(root, text="AI VoiceBox", font=("Arial", 30, "bold"), fg="white", bg="#121212").pack(pady=20)

# Language selection
language_var = tk.StringVar(value="en")
tk.Label(root, text="Select Language", fg="white", bg="#121212", font=("Arial", 14)).pack()

tk.OptionMenu(root, language_var, "en", "hi", "bn").pack(pady=10)

# Button style
btn_style = {
    "width": 30,
    "height": 2,
    "bg": "#1f1f1f",
    "fg": "white",
    "activebackground": "#333333",
    "activeforeground": "white",
    "bd": 0
}

# Buttons
tk.Button(root, text="Hello 👋", command=lambda: speak("Hello"), **btn_style).pack(pady=10)
tk.Button(root, text="I need help 🆘", command=lambda: speak("I need help"), **btn_style).pack(pady=10)
tk.Button(root, text="Thank you 🙏", command=lambda: speak("Thank you"), **btn_style).pack(pady=10)

# Extra buttons (fill screen)
tk.Button(root, text="Emergency 🚨", command=lambda: speak("Help me immediately"), **btn_style).pack(pady=10)
tk.Button(root, text="I am hungry 🍔", command=lambda: speak("I am hungry"), **btn_style).pack(pady=10)
tk.Button(root, text="I am sick 🤒", command=lambda: speak("I am not feeling well"), **btn_style).pack(pady=10)

# Input section
tk.Label(root, text="Type your message:", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 14), bg="#1f1f1f", fg="white", insertbackground="white")
entry.pack(pady=10)

tk.Button(root, text="Speak 🗣️", command=lambda: speak(entry.get()), **btn_style).pack(pady=20)

# Run app
root.mainloop()



#new one 


from gtts import gTTS
from googletrans import Translator
import pygame
import tkinter as tk
import os
import time
import webbrowser
import random
import speech_recognition as sr

translator = Translator()

# ----------- FUNCTIONS -----------

def speak(text):
    try:
        lang = language_var.get()
        
        status_label.config(text="Status: Translating...")
        root.update()
        
        translated = translator.translate(text, dest=lang).text
        
        status_label.config(text="Status: Speaking...")
        root.update()
        
        tts = gTTS(text=translated, lang=lang)
        tts.save("voice.mp3")
        
        pygame.mixer.init()
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.remove("voice.mp3")
        
        status_label.config(text="Status: Ready")
    except Exception as e:
        status_label.config(text="Error!")

# 🎤 Voice Input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, text)
            speak(text)
        except:
            status_label.config(text="Could not understand")

# 🎵 Music
def play_music():
    query = music_entry.get()
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

# 🎮 Game
def start_game():
    game = tk.Toplevel(root)
    game.title("Game 🎮")
    game.geometry("300x300")
    game.configure(bg="black")

    number = random.randint(1, 10)

    tk.Label(game, text="Guess 1-10", fg="white", bg="black").pack(pady=10)
    guess = tk.Entry(game)
    guess.pack()

    result = tk.Label(game, text="", fg="white", bg="black")
    result.pack()

    def check():
        try:
            if int(guess.get()) == number:
                result.config(text="Correct 🎉")
            else:
                result.config(text="Try Again 😢")
        except:
            result.config(text="Enter number")

    tk.Button(game, text="Check", command=check).pack(pady=10)

# ⏰ Clock
def update_time():
    clock.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_time)

# ✨ Animation
def animate():
    color = title.cget("fg")
    title.config(fg="cyan" if color == "white" else "white")
    root.after(500, animate)

# ----------- UI -----------

root = tk.Tk()
root.title("AI VoiceBox")
root.attributes("-fullscreen", True)
root.configure(bg="#121212")

frame = tk.Frame(root, bg="#121212")
frame.pack(expand=True)

tk.Button(root, text="❌ Exit", command=root.destroy, bg="red", fg="white").pack(anchor="ne")

# Title
title = tk.Label(frame, text="AI VoiceBox", font=("Arial", 32, "bold"), fg="white", bg="#121212")
title.pack(pady=10)
animate()

# Clock
clock = tk.Label(frame, font=("Arial", 20), fg="cyan", bg="#121212")
clock.pack()
update_time()

# Status
status_label = tk.Label(frame, text="Status: Ready", fg="lightgreen", bg="#121212")
status_label.pack(pady=5)

# Language
language_var = tk.StringVar(value="en")
tk.OptionMenu(frame, language_var, "en", "hi", "bn").pack(pady=5)

# Buttons
def btn(text, cmd):
    return tk.Button(frame, text=text, command=cmd, width=30, height=2,
                     bg="#1f1f1f", fg="white", bd=0)

btn("Hello 👋", lambda: speak("Hello")).pack(pady=5)
btn("Help 🆘", lambda: speak("I need help")).pack(pady=5)
btn("Emergency 🚨", lambda: speak("Help me immediately")).pack(pady=5)

# Input
entry = tk.Entry(frame, width=40)
entry.pack(pady=5)

btn("Speak 🗣️", lambda: speak(entry.get())).pack(pady=5)
btn("🎤 Voice Input", voice_input).pack(pady=5)

# Music
music_entry = tk.Entry(frame, width=30)
music_entry.pack(pady=5)
btn("🎵 Play Music", play_music).pack(pady=5)

# Game
btn("🎮 Play Game", start_game).pack(pady=10)

root.mainloop()

