"""GUI for sudoku"""

from tkinter import *
from tkinter.simpledialog import askstring
import re
from datetime import timedelta
from sudoku_scraper_and_solver import *
# pylint: disable=[C0301,C0103,W0601,W0614,W0401]

difficulty_of_game = ["easy", "medium", "hard", "expert"]


def game_start(sudoku, solved,difficulty):
    """sets up initial board buttons and numpad"""
    global root
    global my_entries
    global time_count
    global timer

    root=Tk()
    root.title("Sudoku " + difficulty_of_game[difficulty-1])
    root.minsize(400, 400)
    time_count = 0
    make_gameboard(sudoku, solved)
    numpad_input()
    time = Label(root, text='Time', font=("Arial",16))
    time.grid(row=1, column=10)
    timer = Label(root, text = "0:00:00", font=("Arial",16))
    timer.grid(row=2, column=10)
    easy_level=Button(root, text="Easy one", font=("Arial",13), command=lambda : new_starting(1))
    medium_level=Button(root, text="Medium one", font=("Arial",13), command=lambda : new_starting(2))
    hard_level=Button(root, text="Hard one", font=("Arial",13), command=lambda : new_starting(3))
    expert_level=Button(root, text="Expert one", font=("Arial",13), command=lambda : new_starting(4))
    easy_level.grid(row=4, column=10)
    medium_level.grid(row=5, column=10)
    hard_level.grid(row=6, column=10)
    expert_level.grid(row=7, column=10)
    root.after(1000, update_timer)

def numpad_input():
    """crates button inputs for the game"""
    btn_1 = Button(root, bg="orange", text="1", font=("Arial",16), command= lambda: keypad_press("1"))
    btn_2 = Button(root, bg="orange", text="2", font=("Arial",16), command= lambda: keypad_press("2"))
    btn_3 = Button(root, bg="orange", text="3", font=("Arial",16), command= lambda: keypad_press("3"))
    btn_4 = Button(root, bg="orange", text="4", font=("Arial",16), command= lambda: keypad_press("4"))
    btn_5 = Button(root, bg="orange", text="5", font=("Arial",16), command= lambda: keypad_press("5"))
    btn_6 = Button(root, bg="orange", text="6", font=("Arial",16), command= lambda: keypad_press("6"))
    btn_7 = Button(root, bg="orange", text="7", font=("Arial",16), command= lambda: keypad_press("7"))
    btn_8 = Button(root, bg="orange", text="8", font=("Arial",16), command= lambda: keypad_press("8"))
    btn_9 = Button(root, bg="orange", text="9", font=("Arial",16), command= lambda: keypad_press("9"))
    btn_0 = Button(root, bg="orange", text="Clear field", font=("Arial",16), command=lambda: keypad_press("del"))
    btn_1.grid(row=11, column=0)
    btn_2.grid(row=11, column=1)
    btn_3.grid(row=11, column=2)
    btn_4.grid(row=11, column=3)
    btn_5.grid(row=11, column=4)
    btn_6.grid(row=11, column=5)
    btn_7.grid(row=11, column=6)
    btn_8.grid(row=11, column=7)
    btn_9.grid(row=11, column=8)
    btn_0.grid(row=11, column=9)

def keypad_press(arg):
    """writes number from button in proper cell"""
    print(arg)
    pass


def write_entry_into_board(sudoku,solved):
    """
    Fills users inputs into appropriate cell, if it's wrong changes color of numbers in the cell to red
    Checks if endgame condition is met and if it asks for name and surname
    """
    for i in range(9):
        for j in range(9):
            if my_entries[i][j] != 0:
                field = my_entries[i][j]
                value = field.get()
                if len(value)==1 and value >='1' and value<='9':
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
    my_entries=[]
    for i in range(9):
        row_entries = []
        for j in range(9):
            if sudoku[i][j] != 0:
                already_set = Label(root,text=sudoku[i][j],font=("Arial",18))
                already_set.grid(row=i,column=j)
                row_entries.append(0)
            else:
                entry_field = Entry(root,width=3,font=("Arial",18))
                entry_field.bind("<KeyRelease>",lambda event:write_entry_into_board(sudoku,solved))
                entry_field.grid(row=i,column=j)
                row_entries.append(entry_field)
        my_entries.append(row_entries)

def check_filled(sudoku,solved):
    """Checks if endgame condition is met"""
    count_of_wrong = 81
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == solved[i][j]:
                count_of_wrong -= 1
    return count_of_wrong == 0

def saving_solution_to_txt(solution,name):
    """
    saves solution to database if user doesn't give name makes it anonymous by default
    after its saved starts new game
    """
    global root
    global time_count
    if len(name)==0:
        name = "Anonymous-"
    my_new_string = re.sub('[^a-zA-Z]', '-', name) + str(time_count)
    file_name = "./db/"+my_new_string+".txt"
    with open(file_name,'w', encoding = 'utf-8') as file:
        for line in solution:
            file.writelines(str(line)+"\n")
    new_starting()

def new_starting(difficulty=3):
    """makes new game start by default its hard sudoku"""
    root.destroy()
    sudoku_scraped = SudokuScraperAndSolver(difficulty)
    game_start(sudoku_scraped.sudoku,sudoku_scraped.solved,difficulty)


def update_timer():
    """updates timer after every second"""
    global time_count
    time_count += 1
    dis = str(timedelta(seconds=time_count))
    timer.configure(text=dis)
    root.after(1000,update_timer)


game_start(sudoku_scraped_start.sudoku, sudoku_scraped_start.solved, 3)
root.mainloop()
