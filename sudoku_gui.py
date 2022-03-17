from tkinter import *
from tkinter.simpledialog import askstring
import re
from sudoku_scraper_and_solver import *
sudoku=[[0, 0, 5, 0, 0, 0, 0, 0, 0], 
        [7, 0, 4, 0, 0, 3, 0, 0, 6], 
        [0, 0, 0, 7, 2, 1, 0, 4, 0], 
        [6, 7, 2, 0, 0, 0, 0, 5, 0], 
        [0, 0, 0, 0, 8, 0, 0, 0, 0], 
        [0, 8, 0, 0, 0, 0, 1, 7, 2], 
        [0, 2, 0, 1, 5, 0, 0, 0, 0], 
        [5, 0, 0, 8, 0, 0, 6, 0, 3], 
        [0, 0, 0, 0, 0, 0, 2, 0, 0]]



solved=[[2, 9, 5, 6, 4, 8, 7, 3, 1], 
        [7, 1, 4, 5, 9, 3, 8, 2, 6], 
        [8, 3, 6, 7, 2, 1, 5, 4, 9],
        [6, 7, 2, 3, 1, 4, 9, 5, 8], 
        [9, 5, 1, 2, 8, 7, 3, 6, 4], 
        [4, 8, 3, 9, 6, 5, 1, 7, 2], 
        [3, 2, 8, 1, 5, 6, 4, 9, 7], 
        [5, 4, 9, 8, 7, 2, 6, 1, 3], 
        [1, 6, 7, 4, 3, 9, 2, 8, 5]]

    
def game_start(sudoku, solved):
    global root
    root=Tk()
    root.title("Sudoku")
    root.minsize(400,400)
    global my_entries
    make_gameboard(sudoku,solved)
    numpad_input()

def numpad_input():
    dugme_1 = Button(root, bg="orange", text="1", font=("Arial",16), command= lambda: keypad_press("1"))
    dugme_2 = Button(root, bg="orange", text="2", font=("Arial",16), command= lambda: keypad_press("2"))
    dugme_3 = Button(root, bg="orange", text="3", font=("Arial",16), command= lambda: keypad_press("3"))
    dugme_4 = Button(root, bg="orange", text="4", font=("Arial",16), command= lambda: keypad_press("4"))
    dugme_5 = Button(root, bg="orange", text="5", font=("Arial",16), command= lambda: keypad_press("5"))
    dugme_6 = Button(root, bg="orange", text="6", font=("Arial",16), command= lambda: keypad_press("6"))
    dugme_7 = Button(root, bg="orange", text="7", font=("Arial",16), command= lambda: keypad_press("7"))
    dugme_8 = Button(root, bg="orange", text="8", font=("Arial",16), command= lambda: keypad_press("8"))
    dugme_9 = Button(root, bg="orange", text="9", font=("Arial",16), command= lambda: keypad_press("9"))
    dugme_0 = Button(root, bg="orange", text="Clear", font=("Arial",16), command= lambda: keypad_press("del"))
    dugme_1.grid(row=11, column=0)
    dugme_2.grid(row=11, column=1)
    dugme_3.grid(row=11, column=2)
    dugme_4.grid(row=11, column=3)
    dugme_5.grid(row=11, column=4)
    dugme_6.grid(row=11, column=5)
    dugme_7.grid(row=11, column=6)
    dugme_8.grid(row=11, column=7)
    dugme_9.grid(row=11, column=8)
    dugme_0.grid(row=11, column=9)

def keypad_press(arg):
    pass
    

def write_entry_into_board(sudoku,solved):
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
    count_of_wrong = 81
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == solved[i][j]:
                count_of_wrong -= 1
    return count_of_wrong == 0

def saving_solution_to_txt(solution,name):
    global root
    if len(name)==0:
            name = "Anonymous"
    my_new_string = re.sub('[^a-zA-Z]', '-', name)
    # time =datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = "./db/"+my_new_string+".txt"
    with open(file_name,'w', encoding = 'utf-8') as file:
        for line in solution:
            file.writelines(str(line)+"\n")
    root.destroy()
    sudoku_scraped = SudokuScraperAndSolver(3)
    game_start(sudoku_scraped.sudoku,sudoku_scraped.solved)
    
    


game_start(sudoku,solved)
root.mainloop()