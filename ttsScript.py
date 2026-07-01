import sys
import subprocess
import time

# --- Auto-install required modules ---
required_modules = ["pyttsx3", "halo"]

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Installing missing module: {module} ...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip3", "install", module])
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {module}. Please install it manually.")
            sys.exit(1)

# --- Safe imports ---
import pyttsx3
from halo import Halo


def speak(text, delay, rate):
    """Handle text-to-speech with spinner feedback."""
    try:
        with Halo(text="Initializing TTS engine...", spinner="dots") as ttsSpinner:
            engine = pyttsx3.init()
            time.sleep(0.4)
            engine.setProperty("rate", rate)
            engine.setProperty("volume", 1.0)
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[0].id)
            time.sleep(delay)
            ttsSpinner.succeed("TTS engine ready!")

        # Speaking section
        with Halo(text="Speaking...", spinner="dots") as speakSpinner:
            engine.say(text)
            engine.runAndWait()
            speakSpinner.succeed("Finished speaking.")

        engine.stop()

    except Exception as e:
        err = str(e)
        if "ttsSpinner" in locals():
            ttsSpinner.fail(f"Error: {err}")
        else:
            print(f"❌ Error during speech: {err}")


def safe_input(prompt):
    """Wrapper around input() to handle KeyboardInterrupts safely."""
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
        sys.exit(0)


def main():
    try:
        setup_spinner = Halo(text="Setting up TTS...", spinner="dots")
        setup_spinner.start()
        time.sleep(0.5)
        setup_spinner.succeed("TTS Ready! Type anything and it will speak (type 'exit' to quit)\n")

        # Ask for configuration safely
        try:
            rate__ = int(safe_input("Rate of speaking (default 170): ") or 170)
            delay__ = float(safe_input("Delay before speaking (in seconds, default 0.1): ") or 0.1)
        except ValueError:
            rate__, delay__ = 170, 0.1
            print("⚠️ Invalid input detected, using defaults.")

        while True:
            text = safe_input("Say something: ")
            if text.lower() == "exit":
                print("👋 Stopping TTS...")
                break
            elif text.strip() == "":
                print("⚠️ Please enter some text!")
                continue
            speak(text, delay__, rate__)

        print("Goodbye! 👋")

    except KeyboardInterrupt:
        print("\n🛑 Program interrupted.")
        with Halo(text="Exiting program with code 0", spinner="dots"):
            sys.exit(0)

    except Exception as e:
        errorSpinner = Halo(spinner="dots")
        errorSpinner.fail(f"Unexpected error: {e}! Exitng with code 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
