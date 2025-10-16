from gtts import gTTS
import pygame, os, threading

lock = threading.Lock()

def _play(text):
    with lock:  # Only one thread inside at a time
        # Stop any currently playing audio
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        # Save new speech
        path = "voice.mp3"
        gTTS(text=text, lang="en").save(path)

        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        os.remove(path)

def speak(text):
    print(f"Assistant: {text}")
    threading.Thread(target=_play, args=(text,), daemon=True).start()
