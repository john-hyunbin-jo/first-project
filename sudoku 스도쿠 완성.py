import random
from tkinter import * #tkinter

def initialize_board_6x6():
    row0 = [1, 2, 3, 4, 5, 6]
    random.shuffle(row0)
    row1 = [row0[1], row0[0], row0[4], row0[5], row0[2], row0[3]]
    row2 = [row0[2], row0[3], row0[0], row0[4], row0[5], row0[1]]
    row3 = [row0[3], row0[4], row0[5], row0[2], row0[1], row0[0]]
    row4 = [row0[4], row0[5], row0[3], row0[1], row0[0], row0[2]]
    row5 = [row0[5], row0[2], row0[1], row0[0], row0[3], row0[4]]
    board = [row0, row1, row2, row3, row4, row5]
    return board

def shuffle_ribbons(board):
    top = board[:3]
    bottom = board[3:]
    random.shuffle(top)
    random.shuffle(bottom)
    return top + bottom

def transpose(board):
    size = len(board)
    transposed = []
    for _ in range(size):
        transposed.append([])
    for row in board:
        for j in range(size):
            transposed[j].append(row[j])
    return transposed

def create_solution_board_6x6():
    board = initialize_board_6x6()
    board = shuffle_ribbons(board)
    board = transpose(board)
    board = shuffle_ribbons(board)
    board = transpose(board)
    return board

def copy_board(board):
    board_clone = []
    for row in board :
        board_clone.append(row[:])
    return board_clone

def get_level():
    level = input("난이도를 숫자로 입력(초급 1 중급 2 고급 3) : ")
    while level not in ("1","2","3"):
        level = input("난이도를 숫자로 입력(초급 1 중급 2 고급 3) : ")
    if level == "1":
        return 6
    elif level == "2":
        return 8
    else:
        return 10

def make_holes(board, no_of_holes):
    while no_of_holes > 0:
        i = random.randint(0,5)
        j = random.randint(0,5)
        if board[i][j] != 0:
            board[i][j] = 0
            no_of_holes -= 1
    return board

def show_board(board):
    for row in board:
        for entry in row:
            if entry == 0:
                print('.', end=' ')
            else:
                print(entry, end=' ')
        print()     

def get_integer(message,i,j):
    digit = input(message)
    while not (digit.isdigit() and i <= int(digit) <= j):
        digit = input(message)
    return int(digit)



# MAIN --    
solution_board = create_solution_board_6x6()
puzzle_board = copy_board(solution_board)
no_of_holes = get_level()
puzzle_board = make_holes(puzzle_board, no_of_holes)
# show_board(puzzle_board)



# tkinter window 만들기
window = Tk()
window.geometry('480x480') # 창 크기는 480 x 480 (W x H)
window.title('스도쿠 6x6')
# --- 창 속 요소 그리기 ---
mainframe = Frame(window) # 스도쿠 판을 표시할 컨테이너(프레임)
mainframe.pack(side='top')
inputframe = Frame(window, height=60) # 숫자 입력을 받는 컨테이너(프레임)
inputframe.pack(side='bottom')
# 스도쿠 칸 버튼 배열과 선택된 칸 튜플을 담는 변수
sudoku_cells = []
selected_cell = None
# 입력 칸 만들기
def sudoku_cell_try():
    global solution_board
    global sudoku_cells
    global inputbox
    global selected_cell
    global no_of_holes
    comp = int(inputbox.get())
    if solution_board[selected_cell[0]][selected_cell[1]] == comp:
        t = sudoku_cells[6 * selected_cell[0] + selected_cell[1]]
        t['text'] = comp
        t['state'] = DISABLED
        no_of_holes -= 1
    if no_of_holes == 0:
        print('성공하여 게임이 마무리 되었습니다.')
        exit()
    return
inputbox = Entry(inputframe, state=DISABLED)
inputbox.pack(side='left')
inputbutton = Button(inputframe, text='Try', state=DISABLED)
inputbutton.pack(side='right')
inputbutton['command'] = sudoku_cell_try
# 스도쿠 칸이 선택되었을 때 커맨드 함수
def sudoku_cell_clicked(loc):
    global inputbox; global inputbutton; global selected_cell
    inputbox['state'] = NORMAL
    inputbutton['state'] = NORMAL
    selected_cell = loc
    return
# 스도쿠 칸 그리기 (6 x 6)
for row in range(6):
    for col in range(6):
        button = Button(mainframe, text='.' if puzzle_board[row][col] == 0 else puzzle_board[row][col], state=NORMAL if puzzle_board[row][col] == 0 else DISABLED)
        button.grid(row=row, column=col)
        button['command'] = lambda i=row, j=col: sudoku_cell_clicked((i, j)) # ★★★ 버튼마다 커맨드 할당
        sudoku_cells.append(button)
window.mainloop() # 메인루프 실행(창 띄우기 및 실행)