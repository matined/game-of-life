from tkinter import *
import random
import time

SIZE = 700
CELLS_IN_ROW = 35
SPEED = 40


class Cell:
    cells = []
    isPaused = True

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.width = SIZE/CELLS_IN_ROW
        self.pos_x = self.x * self.width
        self.pos_y = self.y * self.width
        self.isAlive = False
        self.create()
        canvas.tag_bind(self.c, "<ButtonPress-1>", self.on_left_click)

    def create(self):
        self.c = canvas.create_rectangle(
            self.pos_x, self.pos_y, self.pos_x+self.width, self.pos_y+self.width, fill="white", outline="red")

    def on_left_click(self, event):
        self.switch_state()

    def switch_state(self):
        if self.isAlive:
            canvas.itemconfig(self.c, fill="white")
        else:
            canvas.itemconfig(self.c, fill="black")
        self.isAlive = not self.isAlive

    def number_of_cells_around(self):
        result = 0
        if Cell.cells[(self.x-1) % CELLS_IN_ROW][(self.y-1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x) % CELLS_IN_ROW][(self.y-1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x+1) % CELLS_IN_ROW][(self.y-1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x+1) % CELLS_IN_ROW][(self.y) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x+1) % CELLS_IN_ROW][(self.y+1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x) % CELLS_IN_ROW][(self.y+1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x-1) % CELLS_IN_ROW][(self.y+1) % CELLS_IN_ROW].isAlive:
            result += 1
        if Cell.cells[(self.x-1) % CELLS_IN_ROW][(self.y) % CELLS_IN_ROW].isAlive:
            result += 1
        return result


def evolve():
    sieve = [[0 for i in range(0, CELLS_IN_ROW)]
             for j in range(0, CELLS_IN_ROW)]

    for i in range(0, CELLS_IN_ROW):
        for j in range(0, CELLS_IN_ROW):
            if Cell.cells[i][j].isAlive and (Cell.cells[i][j].number_of_cells_around() < 2 or Cell.cells[i][j].number_of_cells_around() > 3):
                sieve[i][j] = 1
            if (not Cell.cells[i][j].isAlive) and Cell.cells[i][j].number_of_cells_around() == 3:
                sieve[i][j] = 1

    for i in range(0, CELLS_IN_ROW):
        for j in range(0, CELLS_IN_ROW):
            if sieve[i][j]:
                Cell.cells[i][j].switch_state()


def create_window():
    global window
    window = Tk()
    window.geometry(f"{SIZE}x{SIZE}")
    window.config(bg="white")
    window.resizable(width=False, height=False)

    state = "PAUSED" if Cell.isPaused else "RUNNING"
    window.title(f"Game of Life ({state}, {SPEED/100}s)")

    global canvas
    canvas = Canvas(width=SIZE, height=SIZE,
                    bg="white", highlightthickness=0)
    canvas.pack()


def pause(event):
    if Cell.isPaused:
        for i in Cell.cells:
            for j in i:
                canvas.itemconfig(j.c, outline="black")
    else:
        for i in Cell.cells:
            for j in i:
                canvas.itemconfig(j.c, outline="red")
    Cell.isPaused = not Cell.isPaused

    state = "PAUSED" if Cell.isPaused else "RUNNING"
    window.title(f"Game of Life ({state}, {SPEED/100}s)")


# def increase_time_period(event):
#     global SPEED
#     SPEED += 10
#     state = "PAUSED" if Cell.isPaused else "RUNNING"
#     window.title(f"Game of Life ({state}, {SPEED/100}s)")


# def decrease_time_period(event):
#     global SPEED
#     SPEED -= 10
#     state = "PAUSED" if Cell.isPaused else "RUNNING"
#     window.title(f"Game of Life ({state}, {SPEED/100}s)")


def main():
    create_window()
    window.bind("<space>", pause)
    # window.bind("<Up>", increase_time_period)
    # window.bind("<Down>", decrease_time_period)

    Cell.cells = [[Cell(i, j) for j in range(0, CELLS_IN_ROW)]
                  for i in range(0, CELLS_IN_ROW)]

    i = 0
    while i <= SPEED:
        if i == SPEED:
            if not Cell.isPaused:
                evolve()
            i = 0
        i += 1
        window.update()
        time.sleep(0.01)

    window.mainloop()


if __name__ == "__main__":
    main()
