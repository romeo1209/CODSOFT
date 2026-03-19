import tkinter as tk
from PIL import Image, ImageTk
import random

# -----------------------------
# Window setup
# -----------------------------
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("620x540")
root.resizable(False, False)

# -----------------------------
# Colors
# -----------------------------
BG_COLOR = "#FFC107"
root.configure(bg=BG_COLOR)

# -----------------------------
# Canvas
# -----------------------------
canvas = tk.Canvas(
    root,
    width=600,
    height=280,
    bg=BG_COLOR,
    highlightthickness=2,
    highlightbackground="black"
)
canvas.pack(pady=2)

# -----------------------------
# Image sizes
# -----------------------------
TARGET_SIZE = (150, 150)
BUTTON_SIZE = (100, 100)

# -----------------------------
# Load images
# -----------------------------
left_images = ["rock.jpeg", "paper.jpeg", "scissors.jpeg"]
right_images = ["rock_mirror.jpeg", "paper_mirror.jpeg", "scissors_mirror.jpeg"]

left_hand_imgs = [ImageTk.PhotoImage(Image.open(img).resize(TARGET_SIZE)) for img in left_images]
right_hand_imgs = [ImageTk.PhotoImage(Image.open(img).resize(TARGET_SIZE)) for img in right_images]
button_images = [ImageTk.PhotoImage(Image.open(img).resize(BUTTON_SIZE)) for img in left_images]

# -----------------------------
# Hand positions
# -----------------------------
LEFT_X = 180
RIGHT_X = 420
LEFT_Y = 140
RIGHT_Y = 140

left_hand = canvas.create_image(LEFT_X, LEFT_Y, image=left_hand_imgs[0])
right_hand = canvas.create_image(RIGHT_X, RIGHT_Y, image=right_hand_imgs[0])

canvas.create_text(LEFT_X, LEFT_Y - 100, text="PLAYER", font=("Arial",14,"bold"), fill="black")
canvas.create_text(RIGHT_X, RIGHT_Y - 100, text="CPU", font=("Arial",14,"bold"), fill="black")

# -----------------------------
# Scores
# -----------------------------
player_score = 0
computer_score = 0
max_rounds = 0
current_round = 0

score_frame = tk.Frame(root, bg=BG_COLOR)
score_frame.pack(anchor="w", padx=10)

score_label = tk.Label(
    score_frame,
    text=f"Player: {player_score}  CPU: {computer_score}",
    font=("Arial",16,"bold"),
    fg="yellow",
    bg="black",
    padx=10,
    pady=5
)


score_label.pack()
# horizontal line below scoreboard
# divider = tk.Frame(root, height=2, width=600, bg="black")
# divider.pack(pady=2)



round_label = tk.Label(root,text="",font=("Arial",14,"bold"),bg=BG_COLOR)

# -----------------------------
# Round selection menu
# -----------------------------
start_frame = tk.Frame(root, bg=BG_COLOR)
start_frame.pack(pady=10)

start_label = tk.Label(
    start_frame,
    text="Select Number of Rounds",
    font=("Arial",18,"bold"),
    bg=BG_COLOR
)
start_label.pack(pady=5)

# -----------------------------
# Reset hands
# -----------------------------
def reset_hands():
    canvas.coords(left_hand, LEFT_X, LEFT_Y)
    canvas.coords(right_hand, RIGHT_X, RIGHT_Y)

    canvas.itemconfig(left_hand, image=left_hand_imgs[0])
    canvas.itemconfig(right_hand, image=right_hand_imgs[0])

# -----------------------------
# Shake animation
# -----------------------------
def shake_hands(callback=None, step=0, steps=24):

    if step < steps:

        if step % 2 == 0:
            canvas.move(left_hand, 4, 4)
            canvas.move(right_hand, -4, 4)
        else:
            canvas.move(left_hand, -4, -4)
            canvas.move(right_hand, 4, -4)

        root.after(40, shake_hands, callback, step+1, steps)

    else:
        canvas.coords(left_hand, LEFT_X, LEFT_Y)
        canvas.coords(right_hand, RIGHT_X, RIGHT_Y)

        if callback:
            root.after(150, callback)



# -----------------------------
# Round Counter Animation
# -----------------------------
 
def animate_round_text():

    canvas.itemconfig("round_display", fill="red")

    root.after(150, lambda: canvas.itemconfig("round_display", fill="black"))

# -----------------------------
# Reveal result
# -----------------------------
def reveal_result(player_choice_index):

    global player_score, computer_score, current_round

    choices = ["rock","paper","scissors"]
    computer_choice_index = random.randint(0,2)

    canvas.itemconfig(left_hand,image=left_hand_imgs[player_choice_index])
    canvas.itemconfig(right_hand,image=right_hand_imgs[computer_choice_index])

    player_choice = choices[player_choice_index]
    computer_choice = choices[computer_choice_index]

    if player_choice == computer_choice:
        result_text = "It's a tie!"

    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):

        result_text = "Player wins!"                                
        player_score += 1

    else:
        result_text = "CPU wins!"
        computer_score += 1

    score_label.config(text=f"Player: {player_score}  CPU: {computer_score}")

    canvas.delete("result")

    canvas.create_text(
        300,
        250,
        text=result_text,
        font=("Arial",18,"bold"),
        fill="blue",
        tags="result"
    )

    current_round += 1

    # Early winner detection: if someone has won more than half the rounds,
    # they cannot be beaten — declare the winner immediately.
    # e.g. 3 rounds → 2 wins needed, 5 rounds → 3 wins, 9 rounds → 5 wins
    wins_needed = max_rounds // 2 + 1

    if player_score >= wins_needed:
        show_winner_popup("PLAYER WINS THE GAME!")
        return

    if computer_score >= wins_needed:
        show_winner_popup("CPU WINS THE GAME!")
        return

    if current_round < max_rounds:
        enable_buttons()
        canvas.delete("round_display")

        canvas.create_text(
        10,
        260,
        text=f"Round {current_round+1} / {max_rounds}",
        font=("Arial",12,"bold"),
        fill="black",
        anchor="w",
        tags="round_display"
        )
        animate_round_text()

    if current_round >= max_rounds:

        if player_score > computer_score:
            final_text = "PLAYER WINS THE GAME!"
        elif computer_score > player_score:
            final_text = "CPU WINS THE GAME!"
        else:
            final_text = "GAME TIED!"

        show_winner_popup(final_text)



def disable_buttons():

    for btn in game_buttons:
        btn.config(state="disabled")


def enable_buttons():

    for btn in game_buttons:
        btn.config(state="normal")       

# -----------------------------
# Play round
# -----------------------------
def play_round(player_choice_index):

    if max_rounds == 0:
        return

    if current_round >= max_rounds:
        return

    disable_buttons()

    reset_hands()
    canvas.delete("result")
    shake_hands(lambda: reveal_result(player_choice_index))

# -----------------------------
# Start game
# -----------------------------
def start_game(rounds):
    global max_rounds,current_round,player_score,computer_score

    max_rounds = rounds
    current_round = 0
    player_score = 0
    computer_score = 0

    canvas.delete("round_display")
    canvas.create_text(
        10,
        260,
        text=f"Round 1 / {max_rounds}",
        font=("Arial",12,"bold"),
        fill="black",
        anchor="w",
        tags="round_display"
    )

    score_label.config(text=f"Player: {player_score}  CPU: {computer_score}")

    start_frame.pack_forget()
    button_frame.pack(pady=30)
    enable_buttons()  # <-- make sure buttons are active


# ----------------------------- 
# popup window
# -----------------------------
def show_winner_popup(text):
    popup = tk.Toplevel(root)
    popup.title("Game Over")
    popup.update_idletasks()

    popup_width = 300
    popup_height = 200

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    pos_x = root_x + (root_width // 2) - (popup_width // 2)
    pos_y = root_y + (root_height // 2) - (popup_height // 2)

    popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")
    popup.resizable(False, False)

    # make popup modal
    popup.transient(root)
    popup.grab_set()

    tk.Label(popup, text=text, font=("Arial",16,"bold")).pack(pady=20)

    button_frame_popup = tk.Frame(popup)
    button_frame_popup.pack(pady=10)

    def play_again():
        popup.grab_release()  # release grab before destroying
        popup.destroy()
        restart_game()

    def exit_game():
        popup.grab_release()
        root.destroy()

    tk.Button(button_frame_popup, text="Play Again", font=("Arial",12), width=10,
              command=play_again).grid(row=0,column=0,padx=10)
    tk.Button(button_frame_popup, text="Exit", font=("Arial",12), width=10,
              command=exit_game).grid(row=0,column=1,padx=10)





def restart_game():

        global player_score, computer_score, current_round, max_rounds

        player_score = 0
        computer_score = 0
        current_round = 0
        max_rounds = 0

        score_label.config(text="Player: 0  CPU: 0")
        
        canvas.delete("result")
        canvas.delete("round_display")
        reset_hands()

        
        button_frame.pack_forget()

        # show round selection again
        start_frame.pack(pady=10)
       

# -----------------------------
# Round buttons
# -----------------------------
tk.Button(start_frame,text="3 Rounds",font=("Arial",14),
          command=lambda:start_game(3)).pack(pady=3)

tk.Button(start_frame,text="5 Rounds",font=("Arial",14),
          command=lambda:start_game(5)).pack(pady=3)

tk.Button(start_frame,text="9 Rounds",font=("Arial",14),
          command=lambda:start_game(9)).pack(pady=3)

# -----------------------------
# Game buttons
# -----------------------------
button_frame = tk.Frame(root,bg=BG_COLOR)
game_buttons = []

for i,img in enumerate(button_images):

    btn = tk.Button(
        button_frame,
        image=img,
        command=lambda idx=i:play_round(idx),
        bd=4,
        relief="solid",
        highlightbackground="black",
        highlightcolor="black",
        highlightthickness=2,
        cursor="hand2"
    )

    btn.grid(row=0,column=i,padx=10)
    game_buttons.append(btn)

# -----------------------------
# Run
# -----------------------------
root.mainloop()