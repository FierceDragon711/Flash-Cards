from tkinter import *
import pandas as pd
import random
from tkinter import messagebox
import os
BACKGROUND_COLOR = "#B1DDC6"
#------------------------------------------Read Data----------------------------------------------------#
data_dict = {}
try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    og_data = pd.read_csv("./data/french_words.csv")
    data_dict = og_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

curr_card = {}


def word_generator():
    global curr_card, flip_timer
    window.after_cancel(flip_timer)
    if len(data_dict) == 0:
        canvas.itemconfig(start_text_french, text="Congratulations", fill="grey")
        canvas.itemconfig(start_text_english, text="Please Close", fill="black")
        correct_button.grid_remove()
        incorrect_button.grid_remove()
        os.remove("./data/words_to_learn.csv")
    curr_card = random.choice(data_dict)
    canvas.itemconfig(start_text_french, text="French", fill="grey")
    canvas.itemconfig(start_text_english, text=curr_card["French"], fill="black")
    canvas.itemconfig(card_image, image=canvas_fg)
    flip_timer = window.after(3000, func=flip)


def flip():
    canvas.itemconfig(card_image, image=canvas_bg)
    canvas.itemconfig(start_text_french, text="English", fill="ivory")
    canvas.itemconfig(start_text_english, text=curr_card["English"], fill="white")


def is_known():
    data_dict.remove(curr_card)
    data_update = pd.DataFrame(data_dict)
    data_update.to_csv("./data/words_to_learn.csv", index=False)
    word_generator()


#------------------------------------------UI-----------------------------------------------------------#
window = Tk()
window.title("French Flash Cards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip)
incorrect_image = PhotoImage(file="./images/wrong.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=word_generator)
correct_image = PhotoImage(file="./images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)

canvas_bg = PhotoImage(file="./images/card_back.png")
canvas_fg = PhotoImage(file="./images/card_front.png")
canvas = Canvas(width=800, height=540, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(405, 280, image=canvas_fg)
start_text_french = canvas.create_text(405, 150, text="", font=("Helvetica", 40, "italic"))
start_text_english = canvas.create_text(405, 270, text="", font=("Helvetica", 60, "italic" and "bold"))
canvas.grid(row=0, column=0, columnspan=2)
incorrect_button.grid(row=1, column=0)
correct_button.grid(row=1, column=1)
word_generator()


window.mainloop()