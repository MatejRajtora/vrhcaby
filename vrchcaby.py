import json
import copy
import random

class Stone:
    def __init__(self, Char):
        self.char = Char
    
    def AddStep(args):
     pass

    def Taken(args):
     pass
    
class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class ConsolePlayer(Player):
    pass
class AIPlayer(Player):
    pass

class Game:
    def __init__(self):
        pass
    #layout hrací desky a pozice kamenu
    global gameover
    gameover = False
    global player
    global player1
    global player2
    global columns
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
        
    def move_stone(self, From, To):
        take = columns[From].pop(len(columns[0])-1)
        take.AddStep()
        columns[To].append(take)
        self.check_win()
    
    def dice(self):
        #hození kostky a vrácení hodnot
        dice = []
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if dice1 == dice2:
            dice = [dice1,dice2,dice1,dice2]
        else:
            dice = [dice1,dice2]
        return dice

    def print_board(self):
        max_stones = max(len(point) for point in columns)
        rows = [""] * max_stones
        column_numbers = "ㅤㅤ".join([f"{i+1:2d}" for i in range(len(columns))])
        print(column_numbers)

        for i, point in enumerate(columns, start=1):
            for j in range(max_stones):
                if j < len(point):
                    rows[j] += f"{point[j].char:^6s}"
                else:
                    rows[j] += " " * 6

        for row in rows:
            print(row)
            print("-" * len(row))

    def save(self, arr):
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

    def load(self):
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

    def check_win(self):
        pass
    def switch_player(self, new_player):
        global player
        player = new_player

    def move(self, From, To, player):
        if player.name == "Player 1":
            if columns[To] == []:
                #if columns[To][0].char != player2.symbol:
                        if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.switch_player(player2)
                                self.print_board()
                            else:
                                print("špatný kámen")
                        else:
                            print("Prázdný sloupec")

            elif columns[To][0].char == player2.symbol and len(columns[To]) == 1 :
                    taken = columns[To].pop(0)
                    taken.Taken()
                    if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.switch_player(player2)
                                self.print_board()
                            else:
                                print("špatný kámen")
                    else:
                            print("Prázdný sloupec")
        else:
            print("Neplatný tah")

        if player.name in ("Player 2", "PlayerAI"):
            if columns[To] == []:
                #if columns[To][0].char != player2.symbol:
                        if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.switch_player(player1)
                                self.print_board()
                            else:
                                print("špatný kámen")
                        else:
                            print("Prázdný sloupec")

            elif columns[To][0].char == player1.symbol and len(columns[To]) == 1 :
                    taken = columns[To].pop(0)
                    taken.Taken()
                    if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.switch_player(player1)
                                self.print_board()
                            else:
                                print("špatný kámen")
                    else:
                        print("Prázdný sloupec")
        else:
            print("Neplatný tah")
        
    

    def play(self):
        self.print_board()
        while gameover == False:
                print(player.name)
                print("Odkud:")
                From = int(input())-1
                print("Kam:")
                To = int(input())-1
                if From < To:
                    self.move(From,To, player)
                else:
                     print("Nemůžeš zpátky!")

    #duplikovaní boardu prosave
    #arr = copy.deepcopy(columns)
    
    #test printu
    #print_board()
    #print(columns[0][len(columns[0])-1].char)
    #menu
print('1 for PvP, 2 for PvAI, 3 for load')
gamemode = int(input())
Game = Game()

    
if gamemode == 1:
    player1 = ConsolePlayer("Player 1", "O")
    player2 = ConsolePlayer("Player 2", "X")
    player = player1
    Game.play()

if gamemode == 2:
    player1 = ConsolePlayer("Player 1", "O")
    player2 = AIPlayer("PlayerAI", "X")
    Game.play()

if gamemode == 3:
    Game.load()
    
