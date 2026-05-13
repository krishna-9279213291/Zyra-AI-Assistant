import speech_recognition as sr
import voice
import gui
import brain
import memory

from utils.command_router import execute_command


recognizer = sr.Recognizer()


def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)

            if "zyra" in text:
                return True

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Internet error")

    return False


def start_listening():
    print("Zyra Wake System Started...")

    while True:

        if listen_for_wake_word():

            print("Wake word detected!")

            # GUI popup
            gui.show_gui()

            voice.speak("Yes bhai, bol kya kaam hai")

            # command listen
            command = voice.listen()

            if command:

                print("User:", command)

                # RUN COMMAND ROUTER
                cmd = execute_command(command)

                if cmd:

                    gui.chat.insert(
                        "end",
                        "ZYRA: " + cmd + "\n\n"
                    )

                    voice.speak(cmd)

                else:

                    # AI fallback
                    ai = brain.ask_ai(command)

                    gui.chat.insert(
                        "end",
                        "ZYRA: " + ai + "\n\n"
                    )

                    voice.speak(ai)

            else:
                voice.speak("Kuch suna nahi bhai")

            # GUI auto hide after 10 sec
            gui.root.after(10000, gui.hide_gui)