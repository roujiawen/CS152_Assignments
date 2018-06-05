from Tkinter import *
import tkMessageBox
from go import *
import time

CURRENT_COLOR = "white"
GUI_BOARD_SIZE = 300
SPACE = GUI_BOARD_SIZE/float(BOARD_SIZE)
P_WIDTH = SPACE/2.
PADDING = [P_WIDTH,P_WIDTH, GUI_BOARD_SIZE-P_WIDTH, GUI_BOARD_SIZE-P_WIDTH]
STONE_ORDER = []

def freeze():
    minimax_button.config(state=DISABLED)
    maximin_button.config(state=DISABLED)

def unfreeze():
    minimax_button.config(state=NORMAL)
    maximin_button.config(state=NORMAL)

def toggle_color(event=None):
    global CURRENT_COLOR
    if CURRENT_COLOR == "white":
        CURRENT_COLOR = "black"
        root.config(cursor='dot black black')
    else:
        CURRENT_COLOR = "white"
        root.config(cursor='circle white white')

def draw_board():
    canvas.create_rectangle(*PADDING)
    for i in xrange(1, BOARD_SIZE):
        coord = P_WIDTH+i*SPACE
        # Vertical lines
        canvas.create_line(coord, P_WIDTH, coord, GUI_BOARD_SIZE-P_WIDTH)
        # Horizontal lines
        canvas.create_line(P_WIDTH, coord, GUI_BOARD_SIZE-P_WIDTH, coord)

def draw_number(num, row, column):
    x = P_WIDTH+column*SPACE
    y = P_WIDTH+row*SPACE
    widget = canvas.create_text(x, y, text=str(num), fill="red")

def draw_stone(color, row, column, r=SPACE*0.5*0.9):
    x = P_WIDTH+column*SPACE
    y = P_WIDTH+row*SPACE
    widget = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
    stones[widget] = (row, column)
    canvas.tag_bind(widget, '<ButtonPress-1>', click)

def update_interface(board):
    canvas.delete("all")
    draw_board()
    for i in xrange(BOARD_SIZE):
        for j in xrange(BOARD_SIZE):
            if board[i][j].color == "empty":
                draw_empty(i, j)
            else:
                draw_stone(board[i][j].color, i, j)
    for i, loc in enumerate(STONE_ORDER):
        draw_number(i+1, loc[0], loc[1])

def place_stone(color, loc, num=False):
    board.put(color, loc)
    if num:
        STONE_ORDER.append(loc)
    update_interface(board.board)

def click(event=None):
    i = event.widget.find_closest(event.x, event.y)[0]
    place_stone(CURRENT_COLOR, stones[i])

def draw_empty(row, column, r=SPACE*0.5*0.9):
    x = P_WIDTH+column*SPACE
    y = P_WIDTH+row*SPACE
    widget = canvas.create_oval(x-r, y-r, x+r, y+r, fill=None, width=0)
    stones[widget] = (row, column)
    canvas.tag_bind(widget, '<ButtonPress-1>', click)

def no_possible_move():
    tkMessageBox.showwarning("", "Game Over!/No Solution Found!")


board = Board()
root = Tk()
root.title("Go Game")

######### Controls #########
control_frame = Frame(root)
control_frame.grid(row=0)

def clear_board():
    global STONE_ORDER, board
    STONE_ORDER = []
    board = Board()
    update_interface(board.board)
    unfreeze()

clear_button = Button(control_frame, text="Clear", command=clear_board)
clear_button.grid(row=0, column=0, sticky="ew")

def show_minimax():
    def draw_moves():
        if len(moves) == 0:
            return
        each = moves.pop(0)
        place_stone(each[0], each[1], True)
        root.after(1000, draw_moves)
    moves = iter_deep_minimax(board)
    if len(moves)>0:
        draw_moves()
    else:
        no_possible_move()
    freeze()

minimax_button = Button(control_frame, text="Best Black Move", command=show_minimax)
minimax_button.grid(row=0, column=1, sticky="ew")

def show_maximin():
    def draw_moves():
        if len(moves) == 0:
            return
        each = moves.pop(0)
        place_stone(each[0], each[1], True)
        root.after(1000, draw_moves)
    moves = iter_deep_maximin(board)
    if len(moves)>0:
        draw_moves()
    else:
        no_possible_move()
    freeze()

maximin_button = Button(control_frame, text="Best White Move", command=show_maximin)
maximin_button.grid(row=0, column=2, sticky="ew")

def test(s):
    b = board
    clear_board()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            c = s[i*BOARD_SIZE+j]
            if c == "o":
                place_stone("white", (i,j))
            elif c == "x":
                place_stone("black", (i,j))

def test1():
    s2 = "\
o o o\
 ooox\
oox  \
 xxxx\
x  x "
    test(s2)

test1_button = Button(control_frame, text="Test Case 1", command=test1)
test1_button.grid(row=1, column=0, sticky="ew")

def test2():
    s5_1 = "\
 ox x\
ooxxx\
ox x \
o xxx\
 oo  "
    test(s5_1)

test2_button = Button(control_frame, text="Test Case 2", command=test2)
test2_button.grid(row=1, column=1, sticky="ew")

def test3():
    s3 = "\
 ooo \
ooxoo\
xx xx\
x   x\
xxxxx"
    test(s3)

test3_button = Button(control_frame, text="Test Case 1", command=test3)
test3_button.grid(row=1, column=2, sticky="ew")

######## Instruction ########
instruction = Label(root, text="Press <space> to toggle color; click to place a stone.")
instruction.grid(row=1,pady=5)
######### Canvas #########
canvas = Canvas(root, width=GUI_BOARD_SIZE, height=GUI_BOARD_SIZE)
canvas.grid(row=2)
root.bind("<space>", toggle_color)
stones = {}
draw_board()
for i in xrange(BOARD_SIZE):
    for j in xrange(BOARD_SIZE):
        draw_empty(i, j)

mainloop()
