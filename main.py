"""
Text-based Minesweeper for the Terminal
Made in Python 3
By PseudoMon
Version 1.0
"""

from random import shuffle

def mapping_letters(letters):
    marks = {}
    num = 0
    for letter in letters:
        marks[letter] = num
        num += 1
        
    return marks

def newgame(s=9, numbomb=10):    
    print("\nStarting a new game...")
    
    bomb = {'view': ".", 'bomb': True}
    free = {'view': ".", 'bomb': False}
    all = []    
    
    # Default: 9x9 grid, 81 tiles total, 10 bombs
    for i in range(numbomb):
        all.append(dict(bomb))

    for i in range (s*s - numbomb):
        all.append(dict(free))

    shuffle(all)

    i = 0
    line = []
    grid = []

    for tile in all:
        if i < s:
            line.append(tile)
            i += 1
        if i >= s:
            grid.append(line)
            i = 0
            line = []
            
    return grid
    
def printgrid(grid, letters):
    print("")
    i = 0
    string = "  "

    for num in range(len(grid)):
        string += str(num) + " "

    for row in grid:
        string += "\n" + letters[i] + " "
        for tile in row:
            string += tile['view'] + " "
        i += 1 
        
    print(string)
    
def checkbombs(pos, grid, recursive=False):
    # return True if you opened a bomb
    # baround is number of bombs around you

    # Return if it's out of range
    thistile = postotile(pos, grid, recursive)
    if not thistile:
        return False
           
    # Return if the tile is already opened
    if thistile['view'] != "." and thistile['view'] != "m":
        if not recursive:
            print("Tile is already opened!")
        return False
        
    # If tile is marked, ask if player is sure
    if thistile['view'] == "m":
        if not recursive:
            print("Tile is marked. Are you sure?")
            inp = input("Y/N > ")
            if inp.upper() == "Y":
                pass
            else:
                return
        
    # If it's a bomb
    if thistile['bomb']:
        print("You opened a bomb!")
        thistile['view'] = "B"
        return True
        
    row = pos[0]
    col = pos[1]
    baround = 0
    rows = [row-1, row, row+1]
    cols = [col-1, col, col+1]
    
    for checkrow in rows:
        for checkcol in cols:
            if checkrow < 0 or checkcol < 0:
                pass
            else:
                try:
                    if grid[checkrow][checkcol]['bomb']:
                        loop = False
                        baround += 1
                except IndexError:
                    pass
                    
    thistile['view'] = str(baround)
    
    # If it's 0, check surrounding tiles
    if baround <= 0:
        for checkrow in rows:
            for checkcol in cols:
                if (checkrow >= 0 and checkcol >= 0) and (checkrow, checkcol) != pos:
                    checkbombs((checkrow, checkcol), grid, True)
    else:
        pass
        
    return False
    
def mark(inp, grid):
    inp = inp.split()[1]
    pos = inputtopos(inp) 
    if pos:
        thistile = postotile(pos, grid)
        if not thistile:
            return
            
        if thistile['view'] != ".":
            print("Tile is already opened or marked.")
            return
        thistile['view'] = "m"
        
def unmark(inp, grid):
    inp = inp.split()[1]
    pos = inputtopos(inp)
    if pos:
        thistile = postotile(pos, grid)
        if not thistile:
            return
            
        if thistile['view'] != "m":
            print("Tile is not marked.")
            return
        thistile['view'] = "."
        
def checkwin(grid):
    alldone = True
    for row in grid:
        for tile in row:
            if tile['view'] == ".":
                # Unopened tile
                alldone = False
            elif tile['view'] == "m" and not tile['bomb']:
                # Wrongly marked tile
                alldone = False
                
    return alldone
    
def inputtopos(inp):
    if inp == "x" or inp == "exit":
        return False
        
    elif inp == "":
        return False
        
    elif inp == "help":
        print("Type the address of a tile to open it.")
        print("To mark a tile, type [mark] followed by the address.")
        print("To unmark a tile, type [unmark] followed by the address.")
        print("To see the grid again, type [print].")
        print("Examples: A0, e7, mark D5, unmark d5")
        
    else:    
        inp = inp.upper()
        try:
            pos = ( letter_map[inp[0]], int(inp.strip(inp[0])) )
        except (KeyError, ValueError):
            print("Can't understand input. \nExamples of proper input: A0, e7, mark D5, unmark D5")
            return False
        else:
            return pos
            
def postotile(pos, grid, recursive=False):
    # recursive means it's called from auto-opening, not from player
    try:
        tile = grid[pos[0]][pos[1]]
    except IndexError:
            if not recursive:
                print("Not in range")
            return False
    else:
        return tile
    
           
global letter_map
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"       
letter_map = mapping_letters(letters)

print("Welcome to minesweeper!")
print("Type [help] for possible commands.")

grid = newgame()
printgrid(grid, letters)

gameover = False
inp = None
while inp != "x" and inp != "exit":
    inp = input("> ")
    
    if "print" in inp:
        printgrid(grid, letters)
    
    elif "unmark " in inp:
        unmark(inp, grid)
        printgrid(grid, letters)
    
    elif "mark " in inp:
        mark(inp, grid)
        printgrid(grid, letters)
    
    else:
        pos = inputtopos(inp)
        
        if pos:
            gameover = checkbombs(pos, grid)    
            printgrid(grid, letters)
        
    if gameover:
        grid = newgame()
        printgrid(grid, letters)
        
    elif checkwin(grid):
        print("You won!")
        grid = newgame()
        printgrid(grid, letters)
        
