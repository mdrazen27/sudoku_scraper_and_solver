"""GUI for sudoku"""

#pylint: disable = [C0301,W0601,C0103,W0614,W0401]
from tkinter import *
from tkinter.simpledialog import askstring
import re
from datetime import timedelta
from sudoku_scraper_and_solver import SudokuScraperAndSolver

difficulty_of_game = ["easy", "medium", "hard", "expert"]


def game_start(sudoku, solved,difficulty):
    """sets up initial board buttons and numpad"""
    global root
    global time_count
    global timer
    global frame

    root=Tk()
    root.title("Sudoku " + difficulty_of_game[difficulty-1])
    root.resizable(False,False)
    root.iconbitmap('./static/icon.ico')
    time_count = 0
    frame = Frame(root, bg="black", borderwidth=3)
    frame.grid(row=0, column=0, rowspan=9, columnspan=9)
    make_gameboard(sudoku, solved)
    numpad_input(sudoku,solved)
    time = Label(root, text='Time', font=("Arial",16))
    time.grid(row=1, column=9)
    timer = Label(root, text = "0:00:00", font=("Arial",16))
    timer.grid(row=2, column=9)
    easy_level=Button(root, text="Easy one", bg="SeaGreen4", width=10, font=("Arial",13), command =lambda:new_starting(1))
    medium_level=Button(root, text="Medium one", bg="DarkSeaGreen4", width=10, font=("Arial",13), command =lambda:new_starting(2))
    hard_level=Button(root, text="Hard one", bg="orange red", width=10, font=("Arial",13), command =lambda:new_starting(3))
    expert_level=Button(root, text="Expert one", bg="DarkRed", width=10, font=("Arial",13), command =lambda:new_starting(4))
    easy_level.grid(row=4, column=9)
    medium_level.grid(row=5, column=9)
    hard_level.grid(row=6, column=9)
    expert_level.grid(row=7, column=9)
    root.after(1000, update_timer)

def numpad_input(sudo,solv):
    """crates button inputs for the game"""
    color = "CornflowerBlue"
    btn_1 = Button(root, bg=color, text="1", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"1"))
    btn_2 = Button(root, bg=color, text="2", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"2"))
    btn_3 = Button(root, bg=color, text="3", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"3"))
    btn_4 = Button(root, bg=color, text="4", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"4"))
    btn_5 = Button(root, bg=color, text="5", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"5"))
    btn_6 = Button(root, bg=color, text="6", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"6"))
    btn_7 = Button(root, bg=color, text="7", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"7"))
    btn_8 = Button(root, bg=color, text="8", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"8"))
    btn_9 = Button(root, bg=color, text="9", font=("Arial",16), command= lambda: keypad_press(sudo,solv,"9"))
    btn_del = Button(root, bg=color, text="Clear field", font=("Arial",16), command=lambda: keypad_press(sudo,solv,"del"))
    btn_1.grid(row=11, column=0, sticky="nsew", pady=(3,3))
    btn_2.grid(row=11, column=1, sticky="nsew", pady=(3,3))
    btn_3.grid(row=11, column=2, sticky="nsew", pady=(3,3))
    btn_4.grid(row=11, column=3, sticky="nsew", pady=(3,3))
    btn_5.grid(row=11, column=4, sticky="nsew", pady=(3,3))
    btn_6.grid(row=11, column=5, sticky="nsew", pady=(3,3))
    btn_7.grid(row=11, column=6, sticky="nsew", pady=(3,3))
    btn_8.grid(row=11, column=7, sticky="nsew", pady=(3,3))
    btn_9.grid(row=11, column=8, sticky="nsew", pady=(3,3))
    btn_del.grid(row=11, column=9, sticky="nsew", pady=(3,3))

def keypad_press(sudoku,solved,arg):
    """writes number from button in proper cell"""
    focused_entry = root.focus_get()
    text_inside = focused_entry.get()
    focused_entry.delete(0,END)
    if arg != "del":
        focused_entry.insert(0,text_inside+arg)
    write_entry_into_board(sudoku,solved)

def write_entry_into_board(sudoku,solved):
    """
    Fills users inputs into appropriate cell, if it's wrong changes color of numbers in the cell
    to red. Checks if endgame condition is met and if it asks for name and surname
    """
    for i in range(9):
        for j in range(9):
            if my_entries[i][j] != 0:
                field = my_entries[i][j]
                value = field.get()
                if len(value) == 1 and '1' <= value <= '9':
                    sudoku[i][j] = int(value)
                    if sudoku[i][j] != solved[i][j]:
                        field.configure(foreground= "red")
                    else:
                        field.configure(foreground= "black")
                    if check_filled(sudoku,solved):
                        name = askstring('Way to be remembered', 'Please enter your name and surname.\n')
                        saving_solution_to_txt(sudoku,name)


def make_gameboard(sudoku,solved):
    """Makes initial board"""
    global my_entries
    my_entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            if j in (3,6):
                pad_side = (6,0)
            else:
                pad_side = (1,0)
            if i in (3,6):
                pad_up = (6,0)
            else:
                pad_up = (1,0)
            if sudoku[i][j] != 0:
                already_set = Label(frame, text=sudoku[i][j], font=("Arial",16))
                already_set.grid(row=i, column=j, padx=pad_side, pady=pad_up, sticky="nsew")
                row_entries.append(0)
            else:
                entry_field = Entry(frame, width=3, font=("Arial",18))
                entry_field.bind("<KeyRelease>", lambda event:write_entry_into_board(sudoku,solved))
                entry_field.grid(row=i, column=j, padx=pad_side, pady=pad_up)
                row_entries.append(entry_field)
        my_entries.append(row_entries)

def check_filled(sudoku, solved):
    """Checks if endgame condition is met"""
    count_of_wrong = 81
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == solved[i][j]:
                count_of_wrong -= 1
    return count_of_wrong == 0

def saving_solution_to_txt(solution,name):
    """
    saves solution to database if user doesn't give name makes it anonymous by default,
    after it's saved starts new game
    """
    if len(name) == 0:
        name = "Anonymous_"
    my_new_string = re.sub('[^a-zA-Z]', '_', name) + "_" + str(time_count)
    file_name = "./db/"+my_new_string+".txt"
    with open(file_name,'w', encoding = 'utf-8') as file:
        for line in solution:
            file.writelines(str(line)+"\n")
    new_starting()

def new_starting(difficulty= 3):
    """makes new game start by default its hard sudoku"""
    root.destroy()
    sudoku_scraped = SudokuScraperAndSolver(difficulty)
    game_start(sudoku_scraped.sudoku, sudoku_scraped.solved, difficulty)


def update_timer():
    """updates timer after every second"""
    global time_count
    time_count += 1
    dis = str(timedelta(seconds= time_count))
    timer.configure(text=dis)
    root.after(1000,update_timer)

sudoku_scraped_start = SudokuScraperAndSolver(3)

game_start(sudoku_scraped_start.sudoku, sudoku_scraped_start.solved, 3)
root.mainloop()
