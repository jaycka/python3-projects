import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# ---------------------------------------------------------Read data---------------------------------------------------#
try:
    df = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    df = pd.read_csv('./data/french_words.csv')
    wordlist = df.to_dict(orient='records')
else:
    wordlist = df.to_dict(orient='records')


# ---------------------------------------------------------Flip card---------------------------------------------------#
def flip_card():
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')


# ---------------------------------------------------------Next card---------------------------------------------------#
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(wordlist)
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------------------------------------Next card---------------------------------------------------#
def is_known():
    wordlist.remove(current_card)
    data = pd.DataFrame(wordlist)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


# ---------------------------------------------------------UI Set UP---------------------------------------------------#

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title('Flashy')

flip_timer = window.after(3000, func=flip_card)

card_front_img = PhotoImage(file='./images/card_front.png')
card_back_img = PhotoImage(file='./images/card_back.png')
right_img = PhotoImage(file='./images/right.png')
wrong_img = PhotoImage(file='./images/wrong.png')

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 253, text='', font=('Ariel', 60, 'bold'))

wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()
window.mainloop()
