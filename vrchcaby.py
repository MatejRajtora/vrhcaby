import json
import copy
import random

class Stone:
    def __init__(self, Char):
        self.char = Char
        self.steps =[]
        self.takenOut = 0
    
    def AddStep(self, From, To):
        self.steps.append(To-From)

    def Taken(self):
        self.takenOut+=1
    
class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.takenStones =[]
        self.OutStones =[]


    def AddTakenStone(self, stone):
        self.takenStones.append(stone)

    def AddOutStone(self, stone):
        self.OutStones.append(stone)


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
        take = columns[From].pop(len(columns[From])-1)
        take.AddStep(From, To)
        columns[To].append(take)
        self.check_win()
    
    def throw_dice(self):
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
        if len(player1.OutStones) ==15:
            return player1, True;
        elif len(player2.OutStones) ==15:
            return player2, True;
        return None;

    def check_win_type(self, winner):
        if winner.name == "Player 1":
            if len(player2.OutStones) == 0 and len(player2.takenStones) > 0:
                return "Backgammon"
            elif len(player2.OutStones) == 0:
                return "Gammon"
            elif len(player2.OutStones) < 0:
                return "Klasická"
            else:
                return "Neznámý typ výhry"
        if winner.name == "Player 2":
            if len(player1.OutStones) == 0 and len(player1.takenStones) > 0:
                return "Backgammon"
            elif len(player1.OutStones) == 0:
                return "Gammon"
            elif len(player1.OutStones) < 0:
                return "Klasická"
            else:
                return "Neznámý typ výhry"

            

    def switch_player(self, new_player):
        global player
        player = new_player
    
    def Throw_stone(self,To, player):
        if columns[To] == []:
            columns[To].append(player.takenStones.pop(0))
            self.print_board()
            return True
        elif columns[To][0].char == player.symbol:
            columns[To].append(player.takenStones.pop(0))
            self.print_board()
            return True

        elif columns[To][0].char != player.symbol:
            print("Neplatný vhoz!")
            return False

    def CheckMoveHelp(self, From, To):
        if player.name == "Player 1":
            if To > len(columns)-1:
                positions = self.GetPlayerPositions()
                i =0
                while i < len(positions)-1:
                        if i > len(columns)-7:
                            i+=1
                        else:
                            return False
                        if i == len(positions)-1:
                            return True
        if player.name in ("Player 2", "PlayerAI"):     
            if To < 0:
                    positions = self.GetPlayerPositions()
                    i =0
                    while i < 6:
                            if i < 6:
                                i+=1
                            else:
                                return False
                            if i == 6:
                                return True
            
    def move(self, From, To, player):
        if player.name == "Player 1":
            if To > len(columns)-1:
                positions = self.GetPlayerPositions()
                i =0
                while i < len(positions)-1:
                        if positions[i] > len(columns)-7:
                            i+=1
                        else:
                            print("Nemůžeš vyvádět, dostaň všechny kameny do poslední části")
                            return False
                        if i == len(positions)-1:
                            player.OutStones.append(columns[From].pop(0))
                    
            if columns[To] == []:
                #if columns[To][0].char != player2.symbol:
                        if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.print_board()
                                return True
                            else:
                                print("špatný kámen")
                                return False
                        else:
                            print("Prázdný sloupec")
                            return False
                        
            elif columns[To][0].char == player.symbol:
                    self.move_stone(From, To)
                    self.print_board()
                    return True
            
            elif columns[To][0].char == player2.symbol and len(columns[To]) == 1 :
                    taken = columns[To].pop(0)
                    taken.Taken()
                    player2.AddTakenStone(taken)
                    if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.print_board()
                                return True
                            else:
                                print("špatný kámen")
                                return False
                    else:
                            print("Prázdný sloupec")
                            return False

            else:
                print("Neplatný tah")
                return False
        
        

        if player.name in ("Player 2", "PlayerAI"):
            if To < 0:
                positions = self.GetPlayerPositions()
                i =0
                while i < 6:
                        if positions[i] < 6:
                            i+=1
                        else:
                            print("Nemůžeš vyvádět, dostaň všechny kameny do poslední části")
                            return False
                        if i == 6:
                            player.OutStones.append(columns[From].pop(0))
                    
            if columns[To] == []:
                #if columns[To][0].char != player2.symbol:
                        if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.print_board()
                                return True
                            else:
                                print("špatný kámen")
                                return False
                        else:
                            print("Prázdný sloupec")
                            return False
                        
            elif columns[To][0].char == player.symbol:
                    self.move_stone(From, To)
                    self.print_board()
                    return True

            elif columns[To][0].char == player1.symbol and len(columns[To]) == 1 :
                    taken = columns[To].pop(0)
                    taken.Taken()
                    player1.AddTakenStone(taken)
                    if columns[From] != []:
                            if columns[From][len(columns[From])-1].char == player.symbol:
                                self.move_stone(From, To)
                                self.print_board()
                                return True

                            else:
                                print("špatný kámen")
                                return False

                    else:
                        print("Prázdný sloupec")
                        return False

            else:
                print("Neplatný tah")
                return False

    def GetPlayerPositions(self):
        positions = [] 

        for idx, column in enumerate(columns):
            if  column != [] and column[0].char == player.symbol:
                positions.append(idx)
            

        return positions
    
    def CheckMove(self, dice):
        positions = self.GetPlayerPositions()

        for position in positions:
            for throw in dice:
                if player.symbol == "O":
                    if columns[position+throw] == []:
                        return True
                    elif columns[position+throw][0].char == player.symbol:
                        return True
                    elif self.CheckMoveHelp(position, position-throw):
                        return True
                    elif columns[position+throw][0].char == "X" and columns[position+throw][1] is None:
                        return True
                if player.symbol == "X":
                    if columns[position-throw] == []:
                        return True
                    elif columns[position-throw][0].char == player.symbol:
                        return True
                    elif self.CheckMoveHelp(position, position-throw):
                        return True
                    elif columns[position-throw][0].char == "O" and columns[position-throw][1] is None:
                        return True
        return False
        
        
    def play(self):
        self.print_board()
        dices=[]
        gameover = False
        while gameover == False:
                win = self.check_win()
                if win != None:
                    winner, gameover = win()
                    
                    wintype = self.check_win_type(winner)
                    print("___________________________")
                    print("_________KONEC HRY_________")
                    print("___________________________")
                    print("__VÍTĚZ: ",winner.name,"___")
                    print("__Typ výhry: ",wintype,"___")
                    print("___________________________")
                    gameover = True
                    break 
                if dices == []:
                     hozeno = False
                if hozeno ==False:
                    dices = self.throw_dice()
                    hozeno = True

                print("Na řadě je: ", player.name," (", player.symbol, ")")
                print("Máš vyhozeno ",len(player.takenStones), " kamenů")
                print(f"Kostka hodila/Dostupné tahy: ", dices)
                if self.CheckMove(dices):
                    
                    if len(player.takenStones) > 0:
                        print("Kam chceš položit kámen")
                        Where = int(input())
                        i=0
                        contain2 = False

                        while contain2 == False:

                            if Where == dices[i]:
                                contain2 = True
                                Where2 = Where-1

                                if player.name == "Player 1":
                                    
                                    if self.Throw_stone(Where2, player):
                                        dices.remove(Where)

                                elif player.name in ("Player 2", "PlayerAI"):

                                    if self.Throw_stone(23-Where2, player):
                                        dices.remove(Where)
                                
                            i+=1
                            if i > len(dices):
                                print("Špatně vybraný tah!")
                                break
                                    
                    else:

                        print("Odkud:")
                        From = int(input())-1
                        print("O kolik:")
                        To = int(input())
                        To2 = To
                        i=0
                        contain = False

                        while contain == False:

                            if To == dices[i]:
                                contain=True

                                if player.name in (("Player 2", "PlayerAI")):
                                    To = From-To
                                else:
                                    To = From+To

                            else:
                                i+=1

                            if i == len(dices):
                                print("Špatně vybraný tah!")
                                break

                        if contain:      

                            if (player.name == "Player 1" and From < To) or (player.name in ("Player 2", "PlayerAI") and  From > To):
                                
                                if self.move(From,To, player):
                                    dices.remove(To2)

                                if dices == [] and player.name =="Player 1":
                                    self.switch_player(player2)
                                    
                                elif dices == [] and player.name in ("Player 2", "PlayerAI"):
                                    self.switch_player(player1)

                                else: 
                                    continue
                            else:
                                print("Nemůžeš zpátky!")
                        else:
                            print("Neplatný tah!")
                else:
                    if player.name == "Player 1":
                        print("Hozené neplatané tahy")
                        dices = []
                        self.switch_player(player2)
                    elif player.name in ("Player 2", "PlayerAI"):
                        print("Hozené neplatané tahy")
                        dices = []
                        self.switch_player(player1)

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
    
