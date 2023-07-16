import time
from tkinter import *
from playsound import playsound
import os

# ---------------------------- Audio Set Up --------------------------- #
long_audio = os.path.dirname(__file__) + '/long.mp3'
short_audio = os.path.dirname(__file__) + '/short.mp3'
# ---------------------------- Morse Code Dict ------------------------ #
MORSE_CODE_DICT = {'A': '•-', 'B': '-•••',
                   'C': '-•-•', 'D': '-••', 'E': '•',
                   'F': '••-•', 'G': '--•', 'H': '••••',
                   'I': '••', 'J': '•---', 'K': '-•-',
                   'L': '•-••', 'M': '--', 'N': '-•',
                   'O': '---', 'P': '•--•', 'Q': '--•-',
                   'R': '•-•', 'S': '•••', 'T': '-',
                   'U': '••-', 'V': '•••-', 'W': '•--',
                   'X': '-••-', 'Y': '-•--', 'Z': '--••',
                   '1': '•----', '2': '••---', '3': '•••--',
                   '4': '••••-', '5': '•••••', '6': '-••••',
                   '7': '--•••', '8': '---••', '9': '----•',
                   '0': '-----', ',': '--••--', '.': '•-•-•-',
                   '?': '••--••', '!': '-•-•--'}


# ---------------------------- FUNCTION SETUP -------------------------- #
def english_to_morse(event):
    for _ in morse_code_label:
        morse_code_label[_].config(bg='white', fg='black')
    english = event.widget.get('1.0', END)
    english = english.upper()
    for letter in MORSE_CODE_DICT:
        english = english.replace(letter, MORSE_CODE_DICT[letter])
    morse_code.delete('1.0', END)
    morse_code.insert('1.0', english)
    if event.keysym.upper() in MORSE_CODE_DICT:
        morse_code_label[event.keysym.upper()].config(bg='black', fg='white')


def morse_to_english(event):
    morse = event.widget.get('1.0', END)
    words = morse.strip().replace('.', '•').split(' ')
    message = []
    for word in words:
        message.append([letter for letter in MORSE_CODE_DICT if MORSE_CODE_DICT[letter] == word][0])
    message = ' '.join(message)
    english_text.delete('1.0', END)
    english_text.insert('1.0', message)


def play_sound():
    codes = morse_code.get('1.0', END).strip()
    for code in codes:
        if code == '•':
            playsound(short_audio)
        elif code == '-':
            playsound(long_audio)
        elif code == ' ':
            time.sleep(1)
        time.sleep(0.1)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=5, pady=5, bg='black')
window.attributes('-alpha', '0.8')
window.title('Text to Morse Code Converter')
window.iconbitmap('morse-icon.ico')
# window.overrideredirect(True)

morse_code_label = {}
i = 0
for _ in MORSE_CODE_DICT:
    label = Label(text=f"{_}\n{MORSE_CODE_DICT[_]}", width=5, relief='solid', borderwidth=1)
    label.grid(row=i // 10, column=int(str(i)[-1]))
    morse_code_label[_] = label
    i += 1

english_text = Text(width=50, height=10)
english_text.grid(row=4, column=0, columnspan=10,sticky='EW')
english_text.insert('1.0', 'Enter English to Encode')
window.rowconfigure(4, pad=10)
english_text.bind('<KeyRelease>', english_to_morse)

# morse_code = Label(width=50, height=10)
# morse_code.grid(row=5, column=0, columnspan=10)
# window.rowconfigure(5, pad=10)

morse_code = Text(width=50, height=10)
morse_code.grid(row=5, column=0, columnspan=10, sticky='EW')
morse_code.insert('1.0', 'Enter Morse Code to Decode Separated by Space')
window.rowconfigure(5, pad=10)
morse_code.bind('<KeyRelease>', morse_to_english)

play_button = Button(text='Play', relief='solid', command=play_sound)
play_button.grid(row=6, column=0, columnspan=10, sticky='EW')

window.mainloop()
