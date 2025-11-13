import threading
import pyttsx3
from time import sleep
from config import TTS_RATE, TTS_VOLUME

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.thread = None
        self.is_reading = False
        
    def read_aloud(self, text):
        """Read story aloud in background."""
        if not text or not text.strip():
            return "⚠️ No story to read."
        
        # If already reading, stop it first
        if self.is_reading:
            self.stop()
            sleep(0.2)

        def run_tts():
            try:
                self.engine.stop()
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if any(v in voice.name.lower() for v in ["female", "zira", "samantha"]):
                        self.engine.setProperty('voice', voice.id)
                        break
                self.engine.setProperty('rate', TTS_RATE)
                self.engine.setProperty('volume', TTS_VOLUME)
                self.engine.say(text)
                
                self.engine.startLoop(False)
                while self.is_reading and self.engine.isBusy():
                    self.engine.iterate()
                    sleep(0.1)
                self.engine.endLoop()
                
            except Exception as e:
                print(f"TTS error: {e}")
            finally:
                print("Reading complete")
                self.is_reading = False

        self.is_reading = True
        self.thread = threading.Thread(target=run_tts, daemon=True)
        self.thread.start()
        return "🎙️ Reading story..."

    def stop(self):
        """Stop TTS playback."""
        if self.is_reading:
            try:
                self.is_reading = False
                self.engine.stop()
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=2.0)
                return "🛑 Reading stopped."
            except Exception as e:
                return f"⚠️ Error stopping reading: {e}"
        return "⚠️ No story is currently being read."

# Create singleton instance
tts_service = TTSService()