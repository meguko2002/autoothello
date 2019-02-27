import pyautogui,time

CELL=[]
EDGE=[]
CELL.append(38) #マス1辺の長さ
EDGE.append(28)
CELL.append(38)
EDGE.append(23)

xtop=[]
ytop =[]

try: #盤面の場所を特定
    xtop.append(pyautogui.locateOnScreen('othello.png')[0])
    ytop.append(pyautogui.locateOnScreen('othello.png')[1])
    xtop.append(pyautogui.locateOnScreen('afsgames.png')[0])
    ytop.append(pyautogui.locateOnScreen('afsgames.png')[1])
except :
    print('盤面が初期化されていません')

#8ｘ8のマスを2個定義、各々のマスには(R,G,B)の色を割り当て
masu = [[[0 for i in range(8)] for j in range(8)] for k in range(2)]
for i in range(2):
    for row in range(8):
        for col in range(8):
            center_x = xtop[i] + EDGE[i] + col * CELL[i]
            center_y = ytop[i] + EDGE[i] + row * CELL[i]
            masu[i][row][col] = pyautogui.screenshot().getpixel((int(center_x), int(center_y)))[2]

def detectcolor(i, xtop, ytop, cell, edge):
    for row in range(8):
        for col in range(8):
            center_x = xtop + edge + col * cell
            center_y = ytop + edge + row * cell
            color = pyautogui.screenshot().getpixel((int(center_x), int(center_y)))[2]
            if color != masu[i][row][col]:
                j = 1-i
                # pyautogui.click(xtop[j] + EDGE[j] + col * CELL[j], ytop[j] + EDGE[j] + row * CELL[j])
                masu[i][row][col] = color
                print(masu[i])
                time.sleep(0.5)

while True:
    for i in range(2):
        detectcolor(i, xtop[i], ytop[i], CELL[i], EDGE[i])


# TODO count=0でゲーム開始し、count==80で終了
    #ただしCtr-Cで中断

    # 盤面Ａで、com黒が打つまで待機
    #com黒が打ったらその座標を取得
    # 盤面Ｂで、盤面ＡのCOM黒の位置にpython黒が打つ count++

    # 盤面Ｂで、com白が打つまで待機
    # com白が打ったらその座標を取得
    # 盤面Ａで、盤面ＢのCOM白の位置にpython白が打つ count++