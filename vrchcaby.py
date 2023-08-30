import json
import copy
import random

class Stone:
    def __init__(self, Char):
        self.char = Char
    
class Player:
    #nějakej random pokus co sem zkusil netestovano
    def throw_dice():
        dice = Game.dice()
        print("Hozeno kostkou: ", dice)

class ConsolePlayer(Player):
    pass

class AIPlayer(Player):
    pass

class Game:
   #layout hrací desky a pozice kamenu
    columns = [
            [Stone("O"),Stone("O")],
            [],
            [],
            [],
            [],
            [Stone("X"),Stone("X"),Stone("X"),Stone("X"),Stone("X")],
            [],
            [Stone("X"),Stone("X"),Stone("X")],
            [],
            [],
            [],
            [Stone("O"),Stone("O"),Stone("O"),Stone("O"),Stone("O")],
            [Stone("X"),Stone("X"),Stone("X"),Stone("X"),Stone("X")],
            [],
            [],
            [],
            [Stone("O"),Stone("O"),Stone("O")],
            [],
            [Stone("O"),Stone("O"),Stone("O"),Stone("O"),Stone("O"),],
            [],
            [],
            [],
            [],
            [Stone("X"),Stone("X")]

    ]

    def move_stone(board, from_idx, to_idx):
        #pokus o pohyb - nezkoušeno
        stone = board[from_idx].pop()
        board[to_idx].append(stone)
    
    def dice():
        #hození kostky a vrácení hodnot
        dice = []
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if dice1 == dice2:
            dice = [dice1,dice2,dice1,dice2]
        else:
            dice = [dice1,dice2]
        return dice

    def print_board(board):
        max_stones = max(len(point) for point in board)
        rows = [""] * max_stones
        column_numbers = "ㅤㅤ".join([f"{i+1:2d}" for i in range(len(board))])
        print(column_numbers)

        for i, point in enumerate(board, start=1):
            for j in range(max_stones):
                if j < len(point):
                    rows[j] += f"{point[j].char:^6s}"
                else:
                    rows[j] += " " * 6

        for row in rows:
            print(row)
            print("-" * len(row))

    def save(arr):
        #save do json + převod do stringu aby se to dalo uložit
        array = copy.deepcopy(arr)
        i = 0
        j = 0
        print("Saving....")
        while i < len(array):
            while j < len(array[i]):
                if array[i][j].char == "O":
                    array[i][j] = "O"
                elif array[i][j].char == "X":
                    array[i][j] = "X"
                else:
                    continue
                j+=1
            i+=1
            j=0
        print("Saved!")
        array = json.dumps(array)
        jsonFile = open("save.json", "w")
        jsonFile.write(array)
        jsonFile.close()

    def load():
        #loadovani json + převod zpět na objekty
        print("Loading....")
        f = open("save.json")
        array = json.load(f)
        i = 0
        j = 0
        print(array)
        while i < len(array):
            while j < len(array[i]):
                if array[i][j] == "O":
                    array[i][j] = Stone("O")
                elif array[i][j] == "X":
                    array[i][j] = Stone("X")
                else:
                    continue
                j+=1
            i+=1
            j=0
        
        print("Loaded")

    def play():
        pass
            
    #duplikovaní boardu prosave
    #arr = copy.deepcopy(columns)

    #test printu
    #print_board(columns)

    #menu
    print('1 for PvP, 2 for PvAI, 3 for load')
    x = int(input())
    
    if x == 1:
        player1 = ConsolePlayer()
        player2 = ConsolePlayer()
        play()
    if x == 2:
        player1 = ConsolePlayer()
        player2 = AIPlayer()
        play()
    if x == 3:
        load()
    
