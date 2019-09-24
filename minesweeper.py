import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog, threading
from time import sleep

window = tkinter.Tk()

window.resizable(0, 0)

window.title("Minesweeper")

#prepare default values
gameover = False

#Restart label values
restartDefault = "༼◔‿◔༽" #displayed when game first starts
restartLost = "༼◕︿◕༽"    #displayed when player loses
restartWon = "ヽ༼◔｡◔༽ﾉ"   #displayed when player wins game
restartLabel = tkinter.StringVar()
restartLabel.set(restartDefault)

#Timer values
count = 0
time = tkinter.StringVar()
time.set(count)
firstClick = True

#Declaring game board values and initialising to default "beginner" level
rows = 10
cols = 10
mines = 10

#board refers to the whole area which will contain rowsxcols number of buttons 
board = []
buttons = []
customsizes = []

#Graphics to fill into the cells
colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
mine = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_mine.gif")
flag = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_flag.gif")
tile_no = [" ", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽"]



def timer():
    global count, firstClick, gameover
    while firstClick == False and gameover == False:
        count = count + 1
        time.set(count)
        sleep(1)
        timer()
    restartLabel.set(restartDefault if gameover == False else restartLost)


timeVar = threading.Timer(1.0, timer)

def createMenu():
    menubar = tkinter.Menu(window)
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="Beginner (10x10 with 10 mines)", command=lambda: setSize(10, 10, 10))
    menusize.add_command(label="Intermediate (20x20 with 40 mines)", command=lambda: setSize(20, 20, 40))
    menusize.add_command(label="Expert (35x35 with 120 mines)", command=lambda: setSize(35, 35, 120))
    menusize.add_command(label="custom", command=setCustomSize)
    menusize.add_separator()
    for x in range(0, len(customsizes)):
        menusize.add_command(label=str(customsizes[x][0])+"x"+str(customsizes[x][1])+" with "+str(customsizes[x][2])+" mines", command=lambda customsizes=customsizes: setSize(customsizes[x][0], customsizes[x][1], customsizes[x][2]))
    menubar.add_cascade(label="size", menu=menusize)
    menubar.add_command(label="exit", command=lambda: window.destroy())
    window.config(menu=menubar)


def setCustomSize():
    global customsizes
    r = tkinter.simpledialog.askinteger("Custom size", "Enter amount of rows")
    c = tkinter.simpledialog.askinteger("Custom size", "Enter amount of columns")
    m = tkinter.simpledialog.askinteger("Custom size", "Enter amount of mines")
    while m > r*c:
        m = tkinter.simpledialog.askinteger("Custom size", "Maximum mines for this dimension is: " + str(r*c) + "\nEnter amount of mines")
    customsizes.insert(0, (r,c,m))
    customsizes = customsizes[0:5]
    setSize(r,c,m)
    createMenu()

def setSize(r,c,m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    saveConfig()
    restartGame()

def saveConfig():
    global rows, cols, mines
    #configuration
    config = configparser.SafeConfigParser()
    config.add_section("game")
    config.set("game", "rows", str(rows))
    config.set("game", "cols", str(cols))
    config.set("game", "mines", str(mines))
    config.add_section("sizes")
    config.set("sizes", "amount", str(min(5,len(customsizes))))
    for x in range(0,min(5,len(customsizes))):
        config.set("sizes", "row"+str(x), str(customsizes[x][0]))
        config.set("sizes", "cols"+str(x), str(customsizes[x][1]))
        config.set("sizes", "mines"+str(x), str(customsizes[x][2]))

    with open("config.ini", "w") as file:
        config.write(file)

def loadConfig():
    global rows, cols, mines, customsizes
    config = configparser.SafeConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append((config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)), config.getint("sizes", "mines"+str(x))))

def prepareGame():
    global rows, cols, mines, board
    board = []
    for x in range(0, rows):
        board.append([])
        for y in range(0, cols):
            #add button and init value for game
            board[x].append(0)
    #generate mines
    for _ in range(0, mines):
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        #prevent spawning mine on top of each other
        while board[x][y] == -1:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
        board[x][y] = -1
        if x != 0:
            if y != 0:
                if board[x-1][y-1] != -1:
                    board[x-1][y-1] = int(board[x-1][y-1]) + 1
            if board[x-1][y] != -1:
                board[x-1][y] = int(board[x-1][y]) + 1
            if y != cols-1:
                if board[x-1][y+1] != -1:
                    board[x-1][y+1] = int(board[x-1][y+1]) + 1
        if y != 0:
            if board[x][y-1] != -1:
                board[x][y-1] = int(board[x][y-1]) + 1
        if y != cols-1:
            if board[x][y+1] != -1:
                board[x][y+1] = int(board[x][y+1]) + 1
        if x != rows-1:
            if y != 0:
                if board[x+1][y-1] != -1:
                    board[x+1][y-1] = int(board[x+1][y-1]) + 1
            if board[x+1][y] != -1:
                board[x+1][y] = int(board[x+1][y]) + 1
            if y != cols-1:
                if board[x+1][y+1] != -1:
                    board[x+1][y+1] = int(board[x+1][y+1]) + 1

def prepareWindow():
    global rows, cols, buttons, time
    tkinter.Button(window, textvariable=restartLabel, width = 2, command=restartGame).grid(row=0, column=0, columnspan=int(cols/2), sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    tkinter.Label(window, textvariable=time, ).grid(row = 0, column = cols - (int(cols/2)), columnspan=int(cols/3), sticky = tkinter.N+tkinter.E+tkinter.S+tkinter.W )
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(window, text=" ", width = 2, height = 1, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

def restartGame():
    global gameover, firstClick, count, timeVar, time
    timeVar.cancel()
    gameover = False
    firstClick = True
    count = 0
    time.set(count)
    restartLabel.set(restartDefault)
    sleep(0.5)
    
    #destroy all - prevent memory leak
    for x in window.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    timeVar = threading.Timer(1.0, timer)
    prepareWindow()

def clickOn(x,y):
    global board, buttons, colors, gameover, rows, cols, tile_no, time, firstClick, timeVar, colors
    if firstClick:
        prepareGame()
        firstClick = False
        timeVar.start()
    if gameover:
        return
    buttons[x][y].config(text = str(board[x][y]))
    if board[x][y] == -1:
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        buttons[x][y].config(image = mine, text = "*")
        buttons[x][y].config(background='red')
        gameover = True
        #now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if board[_x][_y] == -1:
                    buttons[x][y]['state'] = 'disabled'
                    buttons[_x][_y].config(image = mine, text = "*")
        tkinter.messagebox.showinfo("Game Over", "You have lost.")
    else:
        buttons[x][y].config(disabledforeground= colors[board[x][y]], text = tile_no[board[x][y]])
    if board[x][y] == 0:
        buttons[x][y].config(text = " ")
        #now repeat for all buttons nearby which are 0... kek
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()

def autoClickOn(x,y):
    global board, buttons, colors, rows, cols, tile_no
    if buttons[x][y]["state"] == "disabled":
        return
    if board[x][y] != 0:
        buttons[x][y].config(text = str(board[x][y]))
    else:
        buttons[x][y].config(text = " ")
    buttons[x][y].config(disabledforeground= colors[board[x][y]], text = tile_no[board[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if board[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1)
        if x != 0:
            autoClickOn(x-1,y)
        if x != 0 and y != cols-1:
            autoClickOn(x-1,y+1)
        if y != 0:
            autoClickOn(x,y-1)
        if y != cols-1:
            autoClickOn(x,y+1)
        if x != rows-1 and y != 0:
            autoClickOn(x+1,y-1)
        if x != rows-1:
            autoClickOn(x+1,y)
        if x != rows-1 and y != cols-1:
            autoClickOn(x+1,y+1)

def onRightClick(x,y):
    global buttons, flag
    if gameover:
        return
    if buttons[x][y]["text"] == "?":
        buttons[x][y].config(image = '', text = " ")
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        for i in range(0, 2): 
            buttons[x][y].config(image = flag, text = "?")
            buttons.image = flag
        buttons[x][y]["state"] = "disabled"

def checkWin():
    global buttons, board, rows, cols, gameover, timeVar, time, firstClick
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if board[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        firstClick = True
        restartLabel.set(restartWon)
        gameover = True
        for _x in range(0, rows):
            for _y in range(cols):
                if board[_x][_y] == -1:
                    buttons[x][y]['state'] = 'disabled'
                    buttons[_x][_y].config(image = mine, text = "*")
        tkinter.messagebox.showinfo("Gave Over", "You have won.")

if os.path.exists("config.ini"):
    loadConfig()
else:
    saveConfig()

createMenu()

prepareWindow()
window.mainloop()