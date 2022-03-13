"""
Sudoku scraping and solving along with interactive Gui
"""

from tkinter import *
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

    def __str__(self):
        return str(self.sudoku)

    def __repr__(self):
        return f'{self.sudoku}'

