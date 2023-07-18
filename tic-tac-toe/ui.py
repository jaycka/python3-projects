from tkinter import *
from tkinter import messagebox
from game import GameBrain
import numpy as np

FONT = ("Arial", 20)
BACKGROUND_COLOR = 'black'
FOREGROUND_COLOR = 'WHITE'


class GameInterface:
    def __init__(self, gamebrain: GameBrain):
        self.game = gamebrain
        self.game_on = True
        self.mode = True
        self.first = True
        self.start = True
        self.turn = 1
        self.window = Tk()

        self.on_img = PhotoImage(file='toggle-on.png')
        self.off_img = PhotoImage(file='toggle-off.png')
        self.human_img = PhotoImage(file='2p.png')
        self.computer_img = PhotoImage(file='1p.png')
        self.cross_img = PhotoImage(file='cross.png')
        self.circle_img = PhotoImage(file='circle.png')
        self.blank = PhotoImage(file='blank.png')
        self.red_cross = PhotoImage(file='red-cross-100.png')
        self.blue_circle = PhotoImage(file='blue-circle-100.png')

        self.player1_img = [self.blue_circle, self.red_cross][self.first]
        self.player2_img = [self.blue_circle, self.red_cross][not self.first]
        self.pc_img = self.player2_img

        self.window.title('Tic Tac Toe')
        self.window.attributes('-alpha', '0.8')
        self.window.config(padx=10, pady=10, bg=BACKGROUND_COLOR)
        self.window.iconbitmap('tic-tac-toe.ico')
        self.window.resizable(False, False)

        self.p2_label = Label(image=self.human_img, bg=BACKGROUND_COLOR)
        self.p2_label.grid(row=0, column=0)

        self.p1_label = Label(image=self.computer_img, bg=BACKGROUND_COLOR)
        self.p1_label.grid(row=0, column=2)

        self.player1_first = Label(image=self.cross_img, bg=BACKGROUND_COLOR)
        self.player1_first.grid(row=1, column=2)

        self.player1_second = Label(image=self.circle_img, bg=BACKGROUND_COLOR)
        self.player1_second.grid(row=1, column=0)

        self.p1_or_p2 = Label(image=self.on_img, bg=BACKGROUND_COLOR)
        self.p1_or_p2.bind('<Button-1>', self.toggle_on)
        self.p1_or_p2.grid(row=0, column=1)

        self.cross_or_circle = Label(image=self.on_img, bg=BACKGROUND_COLOR)
        self.cross_or_circle.bind('<Button-1>', self.first_on)
        self.cross_or_circle.grid(row=1, column=1)

        self.start_button = Button(text='Start', relief=FLAT, command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=3, sticky='EW')
        self.window.rowconfigure(2, pad=30)

        self.build_tiles()

        self.window.columnconfigure(0, uniform='equal')
        self.window.columnconfigure(1, uniform='equal')
        self.window.columnconfigure(2, uniform='equal')

        self.window.mainloop()

    def build_tiles(self):
        self.tile_group = []
        for i in range(self.game.available.shape[0]):
            for j in range(self.game.available.shape[1]):
                self.tile = Button(image=self.blank, relief=SOLID, command=lambda i=i, j=j: self.user_turn(i, j),
                                   state='disabled')
                self.tile.grid(row=i + 3, column=j, sticky='EW')
                self.tile_group.append(self.tile)

    def toggle_on(self, event):
        if self.mode:
            self.p1_or_p2.config(image=self.off_img)
            self.mode = False
        else:
            self.p1_or_p2.config(image=self.on_img)
            self.mode = True

    def first_on(self, event):
        if self.first:
            self.cross_or_circle.config(image=self.off_img)
            self.first = False
        else:
            self.cross_or_circle.config(image=self.on_img)
            self.first = True

    def mark_and_disable_button(self, image, x, y):
        self.tile_group[x * 3 + y].config(image=image, command=LEFT, state="disabled")

    def pc_turn(self):
        x, y = self.game.computer_turn(self.first)
        self.mark_and_disable_button(image=self.pc_img, x=x, y=y)
        if self.game.check_result(not self.first):
            for i in self.tile_group:
                i.config(state='disabled')
            self.game_on = False
            winning_msg = messagebox.showinfo(title='Game finished',
                                              message=f"Player {['o', 'x'][not self.first]} won!")
        elif not np.isnan(self.game.available).any():
            self.game_on = False
            draw_message = messagebox.showinfo(title='Game finished', message='Draw game.')
        print(self.first)

    def user_turn(self, x, y):
        if self.mode:
            self.game.available[x, y] = self.first
            self.mark_and_disable_button(image=self.player1_img, x=x, y=y)
            if self.game.check_result(self.first):
                for i in self.tile_group:
                    i.config(state='disabled')
                self.game_on = False
                winning_msg = messagebox.showinfo(title='Game finished',
                                                  message=f"Player {['o', 'x'][self.first]} won!")
            elif not np.isnan(self.game.available).any():
                self.game_on = False
                draw_message = messagebox.showinfo(title='Game finished', message='Draw game.')
            if self.game_on:
                self.pc_turn()
            # print(self.game.available)
        else:
            if self.turn % 2 == 0:
                self.game.available[x, y] = not self.first
                self.mark_and_disable_button(image=self.player2_img, x=x, y=y)
                if self.game.check_result(not self.first):
                    for i in self.tile_group:
                        i.config(state='disabled')
                    winning_msg = messagebox.showinfo(title='Game finished',
                                                      message=f"Player {['o', 'x'][not self.first]} won!")
                elif not np.isnan(self.game.available).any():
                    draw_message = messagebox.showinfo(title='Game finished', message='Draw game.')
                self.turn += 1

            else:
                self.game.available[x, y] = self.first
                self.mark_and_disable_button(image=self.player1_img, x=x, y=y)
                if self.game.check_result(self.first):
                    for i in self.tile_group:
                        i.config(state='disabled')
                    winning_msg = messagebox.showinfo(title='Game finished',
                                                      message=f"Player {['o', 'x'][self.first]} won!")
                elif not np.isnan(self.game.available).any():
                    draw_message = messagebox.showinfo(title='Game finished', message='Draw game.')
                self.turn += 1

    def start_game(self):
        if self.start:
            self.player1_img = [self.blue_circle, self.red_cross][self.first]
            self.player2_img = [self.blue_circle, self.red_cross][not self.first]
            self.pc_img = self.player2_img

            self.start_button.config(text='Reset')
            self.start = False
            for i in self.tile_group:
                i.config(state='normal')
            # print(self.game.available)
            self.game_on = True
            if not self.first:
                self.pc_turn()

        else:
            self.build_tiles()
            self.turn = 1
            self.game.reset()
            self.start_button.config(text='Start')
            self.start = True
            print(self.game.available)
