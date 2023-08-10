import speech_recognition as sr
import pyttsx3

class SpeechProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak_text(self, command):
        self.engine.say(command)
        self.engine.runAndWait()

    def listen_and_process(self):
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source)

                    user_input = self.recognizer.recognize_google(audio)
                    user_input = user_input.lower()

                    print(user_input)
                    self.speak_text(user_input)

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("Unknown error occurred")

if __name__ == "__main__":
    speech_processor = SpeechProcessor()
    speech_processor.listen_and_process()
