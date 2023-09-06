import json
import copy
import random
from statistics import mean


class Stone:
    def __init__(self, Char):
        self.char = Char
        self.steps =[]
        self.takenOut = 0
    
    def AddStep(self, From, To):
        if From < To:
            self.steps.append(To-From)
        else:
            self.steps.append(From-To)
             

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

class Game:
    def __init__(self):
        pass
    #layout hrací desky a pozice kamenu
    global gameover
    gameover = False
    global player
    player = None
    global player1
    player1 = None

    global player2
    player2 = None

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
        print("Ukládání....")
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
            
        jsdata = {
            "board": array,
            "player": player.name,
            "player1taken": player1.takenStones,
            "player1out": player1.OutStones,
            "player2": player2.name,
            "player2taken": player2.takenStones,
            "player2out": player2.OutStones
        }
        print("Uloženo!")
        jsdata = json.dumps(jsdata)
        jsonFile = open("save.json", "w")
        jsonFile.write(jsdata)
        jsonFile.close()

    def load(self):
        #loadovani json + převod zpět na objekty
        print("Nahrávání....")
        f = open("save.json")
        jsdata = json.load(f)
        i = 0
        j = 0
        array = jsdata["board"]
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

        return [array, jsdata]


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
        elif columns[To][0].char != player.symbol and len(columns[To]) == 1:
            if player.name == "Player 1":
                player2.takenStones.append(columns.pop(len(columns[To])-1))
            elif player.name in ("Player 2", "PlayerAI"):
                player1.takenStones.append(columns.pop(len(columns[To])-1))

            columns[To].append(player.takenStones.pop(0))
            
            self.print_board()
            return True
        elif columns[To][1].char != player.symbol:
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
            if To > len(columns)-1 and columns[From][0].char == "O":
                if columns[From] != []:
                    if columns[From][len(columns[From])-1].char == player.symbol:
                        positions = self.GetPlayerPositions()
                        i =0
                        while i < len(positions)-1:
                                if positions[i] > len(columns)-7:
                                    i+=1
                                else:
                                    print("Nemůžeš vyvádět, dostaň všechny kameny do poslední části")
                                    return False
                        if i == len(positions)-1:
                                    columns[From][len(columns[From])-1].AddStep(From,To)
                                    player.OutStones.append(columns[From].pop(len(columns[From])-1))
                                    self.print_board()
                                    return True
                        else:
                             return False
                    else:
                                print("špatný kámen")
                                return False
                else:
                  
                    print("Prázdný sloupec")
                    return False
                    
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
                    taken = columns[To].pop(len(columns[To])-1)
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
            if To < 0 and columns[From][0].char == "X":
                if columns[From] != []:
                    if columns[From][len(columns[From])-1].char == player.symbol:
                        positions = self.GetPlayerPositions()
                        i =0
                        while i < len(positions)-1:
                                if positions[i] < 6:
                                    i+=1
                                else:
                                    
                                    print("Nemůžeš vyvádět, dostaň všechny kameny do poslední části")
                                    return False
                        if i == len(positions)-1:
                                    columns[From][len(columns[From])-1].AddStep(From,To)
                                    player.OutStones.append(columns[From].pop(len(columns[From])-1))
                                    self.print_board()
                                    return True
                        else:
                             return False
                    else:
                                print("špatný kámen")
                                return False
                else:
                  
                    print("Prázdný sloupec")
                    return False
                    
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
                    taken = columns[To].pop(len(columns[From])-1)
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
                    if position+throw>len(columns)-1:
                        
                        for pos in positions:
                            for dic in dice:
                                i =0
                                if pos+dic >len(columns)-1:
                                    while i < len(positions):
                                        if positions[i] > len(columns)-7:
                                            i+=1
                                        else:
                                            break
                                        if i == len(positions):
                                            return True
                        return False
                         
                    elif columns[position+throw] == []:
                        return True
                    elif columns[position+throw][0].char == player.symbol:
                        return True
                    elif self.CheckMoveHelp(position, position+throw):
                        return True
                    elif columns[position+throw][0].char == "X" and len(columns[position+throw])==1:
                        return True
                if player.symbol == "X":
                    if position+throw>len(columns)-1:
                        for pos in positions:
                            for dic in dice:
                                i =0
                                if pos-dic <0:
                                    while i < len(positions):
                                        if positions[i] < 6:
                                            i+=1
                                        else:
                                            break
                                        if i == len(positions):
                                            return True
                        return False
                    elif not columns[position-throw] or columns[position-throw] == []:
                        return True
                    elif columns[position-throw][0].char == player.symbol:
                        return True
                    elif self.CheckMoveHelp(position, position-throw):
                        return True
                    elif columns[position-throw][0].char == "O" and len(columns[position-throw])==1:
                        return True
        return False
        
    def GetValidMoves(self, dices):
        moves=[]
        positions = self.GetPlayerPositions()

        for position in positions:
            for dice in dices:
                i =0
                if position-dice <0:
                    while i < 6:
                        if positions[i] < 6:
                            i+=1
                        else:
                            break
                        if i == 6:
                            moves.append([position, dice])
                if columns[position-dice] == []:
                        moves.append([position, dice])
                elif columns[position-dice][0].char == player.symbol:
                        moves.append([position, dice])
                elif self.CheckMoveHelp(position, position-dice):
                        moves.append([position, dice])
                elif columns[position-dice][0].char == "O" and len(columns[position-dice])==1:
                        moves.append([position, dice])

        return moves
    
    def GetStats(self):

        p1moves = 0
        p1out = 0
        p1steps = []

        p2moves = 0
        p2out = 0
        p2steps = []


        p1 = copy.copy(player1.OutStones)
        p1.append(player1.takenStones)
        p2 = copy.copy(player2.OutStones)
        p2.append(player2.takenStones)
         
        for column in columns:
            for stone in column:
                if stone.char == "O":
                    p1.append(stone)
                elif stone.char == "X":
                    p2.append(stone)
                     
                
        p1.pop(len(p1)-1)
        p2.pop(0)

        for stone in p1:
            i=0
            while i < len(stone.steps)-1:
                 p1moves +=1
                 i+=1
            j = 0     
            while j < stone.takenOut:
                 p1out +=1
                 j+=1
            k=0
            while k < len(stone.steps):
                p1steps.append(stone.steps[k])
                k+=1

        for stone in p2:
            i=0
            while i< len(stone.steps):
                 p2moves +=1
                 i+=1
            j = 0     
            while j < stone.takenOut:
                 p2out +=1
                 j+=1
            p2steps.append(stone.steps)


        stats = {
              "p1moves": p1moves,
              "p1out": p1out,
              "p2moves": p2moves,
              "p2out": p2out
        }
        self.printStats(stats)
         
    def printStats(self, stats):
         print(player1.name, "Statistiky")
         print("Počet tahů: ", stats["p1moves"])
         print("Počet vyhozených kamenů: ", stats["p1out"])
         print("Životnost kamene na tahy: ", stats["p1moves"]/stats["p1out"])
         print("__________________________")
         print(player2.name, "Statistiky")
         print("Počet tahů: ", stats["p2moves"])
         print("Počet vyhozených kamenů: ", stats["p2out"])
         print("Životnost kamene na tahy: ", stats["p2moves"]/stats["p2out"])



    def play(self):
        self.print_board()
        dices=[]
        moves=[]
        hozeno = False
        gameover = False
        while gameover == False:
                win = self.check_win()
                if win != None:
                    winner, gameover = win
                    
                    wintype = self.check_win_type(winner)
                    print("___________________________")
                    print("_________KONEC HRY_________")
                    print("___________________________")
                    print("\nVÍTĚZ: ",winner.name)
                    print("Typ výhry: ",wintype)
                    print("___________________________")
                    self.GetStats()
                    gameover = True
                    break 
                if dices == []:
                     hozeno = False
                if hozeno ==False:
                    dices = self.throw_dice()
                    hozeno = True

                print("Na řadě je: ", player.name," (", player.symbol, ")")
                print("Máš vyhozeno ",len(player.takenStones), " kamenů")
                print("Máš vyvedeno ",len(player.OutStones), " kamenů")

                print(f"Kostka hodila", dices)
                print( "Možné tahy: ", self.GetValidMoves(dices))
                if self.CheckMove(dices):
                    
                    if len(player.takenStones) > 0:
                        while contain == False and player.name == "PlayerAI":
                            rand = random.randint(0, len(dices)-1);
                            if self.Throw_stone(rand, player):
                                print("PlayerAI položilo kámen na ", rand)
                                contain2 = True
                                dices.remove(Where)
                        if player.name in ("Player 1", "Player 2"):
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

                                elif player.name in ("Player 2"):

                                    if self.Throw_stone(23-Where2, player):
                                        dices.remove(Where)
                                
                            i+=1
                            if i > len(dices):
                                print("Špatně vybraný tah!")
                                break
                                    
                    else:
                        if player.name == "PlayerAI":
                            if moves==[]:
                                moves = self.GetValidMoves(dices)
                            rand = random.randint(0, len(moves)-1)
                            move = moves[rand]
                            if move[1] in dices:
                                if self.move(move[0],move[0]-move[1], player):
                                    dices.remove(move[1])
                                else:
                                    moves.remove(move)
                            else:
                                    moves.remove(move)
                            if dices == []:
                                self.switch_player(player1)


                        else:
                            print("Odkud:")
                            From = input()
                            if From =="ulozit":
                                 self.save(columns)
                                 print("Odkud:")
                                 From = int(input())-1
                            else:
                                 From = int(From)-1
                            print("O kolik:")
                            To = int(input())
                            To2 = To
                            i=0
                            contain = False

                            while contain == False:

                                if To == dices[i]:
                                    contain=True

                                    if player.name in (("Player 2")):
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
print('1 pro PvP, 2 pro PvAI, 3 pro načtení uložené hry')
gamemode = int(input())
Game = Game()

    
if gamemode == 1:
    player1 = Player("Player 1", "O")
    player2 = Player("Player 2", "X")
    player = player1
    Game.play()

if gamemode == 2:
    player1 = Player("Player 1", "O")
    player2 = Player("PlayerAI", "X")
    player = player1
    Game.play()

if gamemode == 3:
    data = Game.load()
    columns = data[0]
    player1 = Player("Player 1", "O")
    player2 = Player(data[1]["player2"], "X")

    player1.takenStones = data[1]["player1taken"]
    player1.OutStones = data[1]["player1out"]

    player2.OutStones = data[1]["player2out"]
    player2.takenStones = data[1]["player2taken"]

    if data[1]["player"] == "Player 1":
            player = player1

    elif data[1]["player"] in ("Player 2", "PlayerAI"):
            player = player2

    print("Nahráno")

    Game.play()
    
