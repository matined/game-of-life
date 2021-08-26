from tkinter import *
import random
import time

SIZE = 800
CELLS_IN_ROW = 40

time_period = 0.5


class Cell:
    number_of_dead_cells = 0

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.c = canvas.create_rectangle(x, y, x+SIZE/CELLS_IN_ROW, y+SIZE/CELLS_IN_ROW,
                                         fill="#F5E6CA")
        self.isAlive = bool(random.getrandbits(1))
        self.lifespan = 1 if self.isAlive else 0
        self.fill()

    def fill(self):
        if self.isAlive:
            if self.lifespan == 1:
                canvas.itemconfig(self.c, fill="#2F5D62")
            else:
                canvas.itemconfig(self.c, fill="#343F56")
        else:
            canvas.itemconfig(self.c, fill="#F5E6CA")

    def number_of_neighbours(self, pos_x, pos_y):
        sum = 0
        if cells[(pos_x-1) % CELLS_IN_ROW][(pos_y) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x+1) % CELLS_IN_ROW][(pos_y) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x) % CELLS_IN_ROW][(pos_y-1) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x) % CELLS_IN_ROW][(pos_y+1) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x-1) % CELLS_IN_ROW][(pos_y-1) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x+1) % CELLS_IN_ROW][(pos_y-1) % CELLS_IN_ROW].isAlive:
            sum += 1
        if cells[(pos_x+1) % CELLS_IN_ROW][(pos_y+1) % CELLS_IN_ROW].isAlive:
            sum += 1
        return sum


def create_window():
    global window
    window = Tk()
    window.geometry(f"{SIZE}x{SIZE}")
    window.config(bg="#F5E6CA")
    window.resizable(width=False, height=False)
    window.title(
        f"Game of Life ({CELLS_IN_ROW}x{CELLS_IN_ROW}, {time_period}s)")


def create_table():
    global canvas
    canvas = Canvas(width=SIZE, height=SIZE,
                    bg="#F5E6CA", highlightthickness=0)
    canvas.pack(side=LEFT)
    global cells
    cells = [[Cell(j, i) for i in range(0, SIZE, SIZE//CELLS_IN_ROW)]
             for j in range(0, SIZE, SIZE//CELLS_IN_ROW)]
    random.seed()


def evolve():
    for x in range(CELLS_IN_ROW):
        for y in range(CELLS_IN_ROW):
            if cells[x][y].isAlive == False and cells[x][y].number_of_neighbours(x, y) == 3:
                cells[x][y].isAlive = True
                cells[x][y].lifespan = 1
            elif cells[x][y].isAlive and cells[x][y].number_of_neighbours(x, y) != 2 and cells[x][y].number_of_neighbours(x, y) != 3:
                cells[x][y].isAlive = False
                cells[x][y].lifespan = 0
            elif cells[x][y].isAlive:
                cells[x][y].lifespan += 1

            cells[x][y].fill()


def increase_time_period(event):
    global time_period
    time_period *= 2
    window.title(
        f"Game of Life ({CELLS_IN_ROW}x{CELLS_IN_ROW}, {time_period}s)")


def decrease_time_period(event):
    global time_period
    time_period /= 2
    window.title(
        f"Game of Life ({CELLS_IN_ROW}x{CELLS_IN_ROW}, {time_period}s)")


create_window()
create_table()

window.bind("<Up>", increase_time_period)
window.bind("<Down>", decrease_time_period)

while True:
    evolve()
    window.update()
    time.sleep(time_period)


window.mainloop()
