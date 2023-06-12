from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    ps = [random.choice(letters) for _ in range(random.randint(8, 10))] + [random.choice(symbols) for _ in
                                                                           range(random.randint(2, 4))] + [
             random.choice(numbers) for _ in range(random.randint(2, 4))]
    random.shuffle(ps)
    ps = ''.join(ps)
    password_entry.delete(0, END)
    password_entry.insert(0, ps)
    pyperclip.copy(ps)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }
    if website == '' or email == '' or password == '':
        messagebox.showwarning(title='Blank Entry', message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open('password_manager.json', 'r') as f:
                data = json.load(f)

        except FileNotFoundError:
            with open('password_manager.json', 'w') as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)
            with open('password_manager.json', 'w') as f:
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    if len(website) != 0:
        try:
            with open('password_manager.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning(title='No File', message='No Data File Found.')
        else:
            if website in data:
                messagebox.showwarning(title=website,
                                       message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}")
            else:
                messagebox.showwarning(title='Not Found', message='No details for the website exists')
        finally:
            website_entry.delete(0, END)
    else:
        messagebox.showwarning(title='Empty Entry', message='Please enter the website.')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=password_img)
canvas.grid(row=0, column=1)

website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

website_entry = Entry()
website_entry.grid(row=1, column=1, columnspan=2, sticky='EW')
website_entry.focus()

email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky='EW')
email_entry.insert(0, 'example@example.com')

password_entry = Entry()
password_entry.grid(row=3, column=1, sticky='EW')

generate_button = Button(text='Generate Password', command=generate_password)
generate_button.grid(row=3, column=2, sticky='EW')

add_button = Button(text='Add', width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky='EW')

search_button = Button(text='Search', command=find_password)
search_button.grid(row=1, column=2, sticky='EW')

window.mainloop()
