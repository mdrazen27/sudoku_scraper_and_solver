"""Sudoku scraping and solving"""

from copy import deepcopy
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class SudokuScraperAndSolver:
    """saves sudoku and solves it using backtracking"""
    def __init__(self,difficulty = 1):
        """
        scrapes sudoku and saves it to new property
        """
        response = requests.get("http://nine.websudoku.com/?level="+str(difficulty))
        soup = BeautifulSoup(response.content,'html.parser')
        soup = soup.find(id="puzzle_grid")
        soup = soup.find_all('input')
        row = 0
        collumn = 0
        sudoku = [[0 for col in range(9)] for row in range(9)]
        for line in soup :
            #goes through all inputs line by line making dictionary out of their attributes
            line = line.attrs
            if collumn == 9:
                collumn = 0
                row += 1
            if 'value' in line.keys():
                sudoku[row][collumn] = int(line["value"])
            collumn += 1
        self.sudoku = sudoku
        cpy = deepcopy(sudoku)
        self.backtracking(cpy)
        self.solved = cpy
        self.saving_solution_to_txt(cpy)


    def __str__(self):
        return str(self.sudoku)

    def __repr__(self):
        return f'{self.sudoku}'

    def check_row_col_block(self,num,position,sudoku):
        """
        checks if number conflicts with one already existing in the same row, column or block
        """
        for i in range(9):
            if sudoku[i][position[1]] == num and i != position[0]:
                return False
            if sudoku[position[0]][i] == num and i != position[1]:
                return False
        for i in range(position[0]//3*3, position[0]//3*3+3):
            for j in range(position[1]//3*3,position[1]//3*3+3):
                if (i,j)!=position and num == sudoku[i][j]:
                    return False
        return True

    def see_next_empty(self,sudoku):
        """checks if any of the blocks is still empty"""
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    return (i, j)
        return False

    def backtracking(self,sudoku):
        """
        if all fields are filled program stops if not it fills all available cells untill conflict
        occurs when it occurs it goes on previos number untill conflict is resolved
        """
        if self.see_next_empty(sudoku):
            row, column = self.see_next_empty(sudoku)
        else:
            return True
        for num in range(1,10):
            if self.check_row_col_block(num,[row,column],sudoku):
                sudoku[row][column] = num
                if self.backtracking(sudoku):
                    return True
                sudoku[row][column] = 0
        return False

    def saving_solution_to_txt(self,solution):
        """saves solution in database with unique time of solution"""
        time =datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = "./db/automatic-result-"+time+".txt"
        with open(file_name,'w', encoding = 'utf-8') as file:
            for line in solution:
                file.writelines(str(line)+"\n")

sudoku_scraped_start = SudokuScraperAndSolver(3)
