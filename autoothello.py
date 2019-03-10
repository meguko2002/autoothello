import pyautogui, time
BOARD_SIZE = 8
TOUT = 5
BLACK = 0
WHITE = 1
COL_ID = 'abcdefgh' #行番号をa～hに対比

#先手 BLACKの盤面
board_a = {'template': 'othello.png', 'cellsize': 38, 'edge': 28, \
           'start_x': 356, 'start_y': 238}
#後手 WHITEの盤面
board_b = {'template': 'afsgames.png', 'cellsize': 38, 'edge': 23, \
           'pass_x': 47, 'pass_y': 379}

"""screen position(x,y)  board position(col,row)"""

def add_topposition(board):
    board['xtop'], board['ytop'], w, h = pyautogui.locateOnScreen(board['template'])

def add_stone_color(board):
    white = getcolor(board, 3, 3)
    black = getcolor(board, 3, 4)
    board['white'] = white
    board['black'] = black

def getcolor(board, col, row, offset=5):
    x, y = board2screen(board, col, row)
    a = pyautogui.screenshot().getpixel((x+offset, y+offset))
    return a

def board2screen(board, col, row):
    x = board['xtop'] + board['edge'] + col * board['cellsize']
    y = board['ytop'] + board['edge'] + row * board['cellsize']
    return int(x), int(y)

def putstone(board, col, row): #put a stone on a board
    x, y = board2screen(board, col, row)
    pyautogui.click(x, y)
    return True

def detectchange(board, stonecolor):
    global crow,ccol
    temppos = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if blankcells[row][col] == 1:
                color = getcolor(board, col, row)[0]
                if color == board[stonecolor][0]:
                    temppos.append([col, row])
    if len(temppos) == 2:
        for pair in temppos:
            # board_bで黒連続打ちの際、先に打たれた「赤十時でない石」を選択
            if getcolor(board,pair[0], pair[1], offset=0)[0] == 0:
                crow = pair[1]
                ccol = pair[0]
        blankcells[crow][ccol] = 0
        return True
    elif len(temppos) == 1:
        crow = temppos[0][1]
        ccol = temppos[0][0]
        blankcells[crow][ccol] = 0
        return True
    elif len(temppos) > 2:
        raise Exception('multi stone error')

def push_pass(board):
    psx = board['xtop'] + board['pass_x']
    psy = board['ytop'] + board['pass_y']
    pyautogui.click(psx, psy)

def push_start(board):
    psx = board['xtop'] + board['start_x']
    psy = board['ytop'] + board['start_y']
    pyautogui.click(psx, psy)

print('initializing...')
add_topposition(board_a)
add_topposition(board_b)
add_stone_color(board_a)
add_stone_color(board_b)

# 駒が置かれているところは１、それ以外は0
blankcells = [[1 for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
blankcells[3][3] = 0
blankcells[3][4] = 0
blankcells[4][3] = 0
blankcells[4][4] = 0

counter =0 #トータル手数counter初期値は以下の計算で60になるはず
for cols in blankcells:
    counter += sum(cols)

crow = 0
ccol = 0

print('start!')
start_time = time.time()
rap_time = 0
push_start(board_a)
turn = BLACK
while counter > 0:
    if detectchange(board_a, 'black'):
        print('{0} 黒({1}, {2})'.format(61-counter, COL_ID[ccol], crow + 1))
        putstone(board_b, ccol, crow)
        while True:
            putstone(board_b, ccol, crow)
            if getcolor(board_b, ccol, crow) == board_b['black']:
                break
        counter -= 1
        # print(' ' + str(counter) + 'left')
        turn = WHITE

    if detectchange(board_b, 'white'):
        print('{0} 白({1}, {2})'.format(61-counter, COL_ID[ccol], crow + 1))
        putstone(board_a, ccol, crow)
        while True:
            if getcolor(board_a, ccol, crow) == board_a['white']:
                break
        counter -= 1
        # print(' ' + str(counter) + 'left')
        rap_time = time.time()
        turn = BLACK
    duration = time.time() - rap_time
    if (turn == BLACK) & (duration > TOUT):  # board_bでplayerパスのとき
        push_pass(board_b)
        rap_time = time.time()
    # TODO timeout処理
    # TODO Ctr-C 割り込み終了
    # TODO イニシャライズ失敗時のエラー処理

print('game over   raptime={:.2f}[sec]'\
      .format(time.time()-start_time))

