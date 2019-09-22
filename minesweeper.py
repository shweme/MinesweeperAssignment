import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog, threading
from time import sleep

window = tkinter.Tk()

window.resizable(0, 0)

window.title("Minesweeper")

#prepare default values

rows = 10
cols = 10
mines = 10

count = 0
time = tkinter.StringVar()
time.set(count)
firstClick = True

field = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
plain = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_clicked.gif")
mine = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_mine.gif")
flag = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_flag.gif")
tile_no = []
for x in range(1, 9):
    tile_no.append(tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_"+str(x)+".gif"))

gameover = False
customsizes = []

def timer():
    global time, count, timeVar, firstClick
    while firstClick == False:
        count = count + 1
        time.set(count)
        sleep(1)
        timer()
    timeVar.cancel()


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
    global rows, cols, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            #add button and init value for game
            field[x].append(0)
    #generate mines
    for _ in range(0, mines):
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        #prevent spawning mine on top of each other
        while field[x][y] == -1:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
        field[x][y] = -1
        if x != 0:
            if y != 0:
                if field[x-1][y-1] != -1:
                    field[x-1][y-1] = int(field[x-1][y-1]) + 1
            if field[x-1][y] != -1:
                field[x-1][y] = int(field[x-1][y]) + 1
            if y != cols-1:
                if field[x-1][y+1] != -1:
                    field[x-1][y+1] = int(field[x-1][y+1]) + 1
        if y != 0:
            if field[x][y-1] != -1:
                field[x][y-1] = int(field[x][y-1]) + 1
        if y != cols-1:
            if field[x][y+1] != -1:
                field[x][y+1] = int(field[x][y+1]) + 1
        if x != rows-1:
            if y != 0:
                if field[x+1][y-1] != -1:
                    field[x+1][y-1] = int(field[x+1][y-1]) + 1
            if field[x+1][y] != -1:
                field[x+1][y] = int(field[x+1][y]) + 1
            if y != cols-1:
                if field[x+1][y+1] != -1:
                    field[x+1][y+1] = int(field[x+1][y+1]) + 1

def prepareWindow():
    global rows, cols, buttons, time
    tkinter.Button(window, text="Restart", width = 2, command=restartGame).grid(row=0, column=0, columnspan=cols-3, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    tkinter.Label(window, textvariable=time).grid(row = 0, column = cols-3, columnspan=3, sticky = tkinter.N+tkinter.E+tkinter.S+tkinter.W )
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
    sleep(3)
    
    #destroy all - prevent memory leak
    for x in window.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    prepareWindow()

def clickOn(x,y):
    global field, buttons, colors, gameover, rows, cols, tile_no, plain, time, firstClick, timeVar
    if firstClick:
        prepareGame()
        firstClick = False
        timeVar.start()
    if gameover:
        return
    buttons[x][y].config(text = str(field[x][y]))
    if field[x][y] == -1:
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        buttons[x][y].config(image = mine, text = "*")
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        tkinter.messagebox.showinfo("Game Over", "You have lost.")
        #now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[x][y]['state'] = 'disabled'
                    buttons[_x][_y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
                    buttons[_x][_y].config(image = mine, text = "*")
    else:
        buttons[x][y].config(image = tile_no[(field[x][y] - 1)] if field[x][y] > 0 else plain)
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    if field[x][y] == 0:
        buttons[x][y].config(image = plain, text = " ")
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        #now repeat for all buttons nearby which are 0... kek
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()

def autoClickOn(x,y):
    global field, buttons, colors, rows, cols, tile_no, plain
    if buttons[x][y]["state"] == "disabled":
        return
    if field[x][y] != 0:
        buttons[x][y].config(text = str(field[x][y]))
    else:
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        buttons[x][y].config(image = plain, text = " ")
    buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    buttons[x][y].config(image = tile_no[(field[x][y] - 1)] if field[x][y] > 0 else plain)
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if field[x][y] == 0:
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
    global buttons, plain, flag
    if gameover:
        return
    if buttons[x][y]["text"] == "?":
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        buttons[x][y].config(image= plain, text = " ")
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
        buttons[x][y].config(image = flag, text = "?")
        buttons[x][y]["state"] = "disabled"

def checkWin():
    global buttons, field, rows, cols, gameover, timeVar, time
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        tkinter.messagebox.showinfo("Gave Over", "You have won.")
        gameover = True
        timeVar.cancel()
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[x][y]['state'] = 'disabled'
                    buttons[_x][_y].grid(sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
                    buttons[_x][_y].config(image = mine, text = "*")


if os.path.exists("config.ini"):
    loadConfig()
else:
    saveConfig()

createMenu()

prepareWindow()
window.mainloop()