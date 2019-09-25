#import statements
import tkinter, configparser, tkinter.messagebox, tkinter.simpledialog 
import random, os, threading
from time import sleep


#creating game window and setting title and icon
window = tkinter.Tk()
window.title("Minesweeper")
window.iconbitmap("MinesweeperAssignment/images/Flag.ico")

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
customsizes = [] #array that stores all board customisations made for future use

#Graphics to fill into the cells
colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
mine = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_mine.gif")
flag = tkinter.PhotoImage(file = "MinesweeperAssignment/images/tile_flag.png")
tile_no = [" ", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽"]


#function for timer label
def timer():
    global count, firstClick, gameover
    while firstClick == False and gameover == False:
        count = count + 1
        time.set(count)
        sleep(1)
        timer()

#threading variable
timeVar = threading.Timer(1.0, timer)


#This function creates the menu bar which includes:
def createMenu():
    menubar = tkinter.Menu(window)
    # settings to change board size, and
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="Beginner (10x10 with 10 mines)", command=lambda: setSize(10, 10, 10))
    menusize.add_command(label="Intermediate (20x20 with 40 mines)", command=lambda: setSize(20, 20, 40))
    menusize.add_command(label="Expert (35x35 with 120 mines)", command=lambda: setSize(35, 35, 120))
    menusize.add_command(label="custom", command=setCustomSize)
    menusize.add_separator()
    for x in range(0, len(customsizes)):
        menusize.add_command(label=str(customsizes[x][0])+"x"+str(customsizes[x][1])+" with "+str(customsizes[x][2])+" mines", command=lambda customsizes=customsizes: setSize(customsizes[x][0], customsizes[x][1], customsizes[x][2]))
    menubar.add_cascade(label="size", menu=menusize)
    # a close window option
    menubar.add_command(label="exit", command=lambda: window.destroy())
    window.config(menu=menubar)


#this function allows user to enter desired board dimensions and number of mines
def setCustomSize():
    global customsizes
    r = tkinter.simpledialog.askinteger("Custom size", "Enter amount of rows")
    c = tkinter.simpledialog.askinteger("Custom size", "Enter amount of columns")
    m = tkinter.simpledialog.askinteger("Custom size", "Enter amount of mines")
    #number of mines need to be proportionate to board dimensions
    while m > r*c:
        m = tkinter.simpledialog.askinteger("Custom size", "Maximum mines for this dimension is: " + str(r*c) + "\nEnter amount of mines")
    customsizes.insert(0, (r,c,m))
    customsizes = customsizes[0:5]
    setSize(r,c,m)
    createMenu()


#sets values for rows. columns, and mines for system to remember
def setSize(r,c,m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    saveConfig()
    restartGame()


#saves any customizations made to game as options for future
def saveConfig():
    global rows, cols, mines
    #configuration
    config = configparser.ConfigParser()
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


#when game is being reloaded, loads last played board dimensions and mines
#as well as any previous board customisations
def loadConfig():
    global rows, cols, mines, customsizes
    config = configparser.ConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append((config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)), config.getint("sizes", "mines"+str(x))))


#spawns mines and makes sure that mines don't spawn on top of each other
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


#setup for board display
def prepareWindow():
    global rows, cols, buttons, time
    restartButton = tkinter.Button(window, textvariable=restartLabel, width = 2, command=restartGame).grid(row=0, column=0, columnspan=int(cols/2), sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    timerLabel= tkinter.Label(window, textvariable=time, font=("Times", 10, "bold"))
    timerLabel.grid(row = 0, column = cols - (int(cols/2)), columnspan=int(cols/2), sticky = tkinter.N+tkinter.E+tkinter.S+tkinter.W)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(window, text=" ", width = 2, height = 1, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)


#when the restart button is clicked, resets vital game values
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


#this function executes when a button(cell) is clicked on
def clickOn(x,y):
    global board, buttons, colors, gameover, rows, cols, tile_no, time, firstClick, timeVar, colors, restartLost
    #checks if this is the first click of the game to 
    if firstClick:
        #randomly assign mines on the board after first click
        prepareGame()
        #toggle value so this only happens once per game
        firstClick = False
        #AND start the game timer
        timeVar.start()
    if gameover:
        return
    buttons[x][y].config(text = str(board[x][y]))
    #checks if clicked cell is a mine
    if board[x][y] == -1:
        #displays mine if it is one
        buttons[x][y].config(image = mine, text = "*", background='red')
        #sets Lose condition
        gameover = True
        #now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if board[_x][_y] == -1:
                    if buttons[_x][_y]["text"] == "?":
                        buttons[_x][_y].config(background = 'green')
                    elif buttons[_x][_y]["text"] != "?":
                        buttons[_x][_y].config(image = mine, text = "*")
                elif board[_x][_y] != -1 and buttons[_x][_y]["text"] == "?":
                    buttons[_x][_y].config(background = 'red')
                buttons[x][y]['state'] = 'disabled'
        restartLabel.set(restartLost) #changes Restart button to lost emoticon and displays game ove
        tkinter.messagebox.showinfo("Game Over", "You have lost.")
    else: #displays any and all surrounding numbers if not a mine
        buttons[x][y].config(disabledforeground= colors[board[x][y]], text = tile_no[board[x][y]])
    if board[x][y] == 0: #displays "pocket" which has no mine around
        buttons[x][y].config(text = " ")
        #repeats for all surrounding cells to reveal empty pockets, if any exist
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled' #after a button has been clicked on, it cannot be clicked again
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()#checks if player has won after every cell click


#function that has been set up to reveal pockets of cells that have no mines around
def autoClickOn(x,y):
    global board, buttons, colors, rows, cols, tile_no
    if buttons[x][y]["state"] == "disabled":
        return #if button has already been clicked or flagged, do nothing to it
    if board[x][y] != 0: #gets board values
        buttons[x][y].config(text = str(board[x][y]))
    else:#sets "pockets" to display nothing
        buttons[x][y].config(text = " ")
    #display valid surrounding numbers and disable these buttons
    buttons[x][y].config(disabledforeground= colors[board[x][y]], text = tile_no[board[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    #repeats the same for the 8 cells surrounding button[x][y] if current cell is a "pocket"
    #   N.W.      N        N.E.  #
    #   W         0          E   #
    #   S.W.      S        S.E.  #

    if board[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1) #checking N.W.
        if x != 0:
            autoClickOn(x-1,y) #checking W
        if x != 0 and y != cols-1:
            autoClickOn(x-1,y+1) #checking S.W. 
        if y != 0:
            autoClickOn(x,y-1) #checking N
        if y != cols-1:
            autoClickOn(x,y+1) #checking S
        if x != rows-1 and y != 0:
            autoClickOn(x+1,y-1) #chekcing N.E.
        if x != rows-1:
            autoClickOn(x+1,y) #checking E
        if x != rows-1 and y != cols-1:
            autoClickOn(x+1,y+1) #checking S.E.


#function that toggles between displaying a flag and "unflagging" when a cell is right clicked 
def onRightClick(x,y):
    global buttons, flag
    if gameover:
        return
    #If button is a flag, "unflags" that cell
    if buttons[x][y]["text"] == "?":
        buttons[x][y].config(image = '', text = " ")
        buttons[x][y]["state"] = "normal"
    #else, flags the cell if cell is unflagged
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        #buttons[x][y]["state"] = "disabled"
        for i in range(0, 2):
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].config(image = flag, text = "?")
        
        
#function checkWin is called everytime a cell is clicked on to check if win conditions have been met
def checkWin():
    global buttons, board, rows, cols, gameover, timeVar, time, firstClick, restartWon
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            #checks if all non-mine cells have been revealed
            if board[x][y] != -1 and buttons[x][y]["state"] == "normal":
                #If even one non-mine cell is not revealed, win condition is set to false
                win = False
    if win:
        #if all non-mine cells have been revealed, starts gameover process and reveals all mines
        firstClick = True
        gameover = True
        for _x in range(0, rows):
            for _y in range(cols):
                if board[_x][_y] == -1:
                    if buttons[_x][_y]["text"] == "?":
                        buttons[_x][_y].config(background = 'green')
                    elif buttons[_x][_y]["text"] != "?":
                        buttons[_x][_y].config(image = mine, text = "*")
                elif board[_x][_y] != -1 and buttons[_x][_y]["text"] == "?":
                    buttons[_x][_y].config(background = 'red')
                buttons[x][y]['state'] = 'disabled'
        restartLabel.set(restartWon)
        tkinter.messagebox.showinfo("Game Over", "You have won")

#loading configuration file for game 
if os.path.exists("config.ini"):
    loadConfig()
else:#saving config to file config.ini if one doesn't already exist
    saveConfig()

#main game area that sets up th game and then loops the window to reflect any changes
createMenu()
prepareWindow()
window.mainloop()