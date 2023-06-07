from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = '🗹'

reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    timer_label.config(text='Timer', fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0
    check_label.config(text=CHECK_MARK * (reps // 2))


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        timer_label.config(text='Break', fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        timer_label.config(text='Break', fg=PINK)
        count_down(short_break_sec)
    else:
        timer_label.config(text='Work', fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_minute = count // 60
    count_second = count % 60
    canvas.itemconfig(timer_text, text=f"{count_minute:02d}:{count_second:02d}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        check_label.config(text=CHECK_MARK * (reps // 2))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Pomodoro')
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text='Timer', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, 'bold'))
timer_label.grid(row=0, column=1)

check_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 24))
check_label.grid(row=3, column=1)

start_button = Button(text='Start', highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text='Reset', highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, 'bold'))
canvas.grid(row=1, column=1)

window.mainloop()
