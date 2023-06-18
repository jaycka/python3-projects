from tkinter import *


def calc():
    result['text'] = round(float(entry.get()) * 1.609, 1)


window = Tk()
window.title('Mile to Km Converter')
window.config(padx=20, pady=20)

Label(text='is equal to', font=('Ariel', 12), padx=10, pady=10).grid(row=1, column=0)
Label(text='Miles', font=('Ariel', 12), padx=10, pady=10).grid(row=0, column=2)
Label(text='Km', font=('Ariel', 12), padx=10, pady=10).grid(row=1, column=2)

result = Label(text=0, font=('Ariel', 12), padx=10, pady=10)
result.grid(row=1, column=1)

entry = Entry(width=7, font=('Ariel', 12))
entry.insert(END, 0)
entry.grid(row=0, column=1)

button = Button(text='Calculate', command=calc, font=('Ariel', 12), padx=10, pady=10)
button.grid(row=2, column=1)

window.mainloop()
