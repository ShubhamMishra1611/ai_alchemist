import re

class MarkupInterpreter:
    def __init__(self):
        pass

    def interpret_bold(self, text):
        return re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)

    def interpret_code(self, text):
        return re.sub(r'`(.*?)`', r'\033[4m\1\033[0m', text)

    def interpret_markup(self, text):
        text = self.interpret_bold(text)
        text = self.interpret_code(text)
        return text

if __name__ == "__main__":
    markup_interpreter = MarkupInterpreter()

    bold_text = "this is **bold** text"
    code_text = "this is `code` text"
    bullet_text = "*this* is a bullet point"
    combined = bold_text + "\n" + code_text + "\n" + bullet_text
    interpreted_text = markup_interpreter.interpret_markup(combined)
    print(interpreted_text)
