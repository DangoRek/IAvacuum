from os import system, name
from time import sleep
from random import randint

SPEED = 100
SLEEP = 1/SPEED

LEVEL_WIDTH = 30
LEVEL_HEIGHT = 15
WALL_PROBABILITY = 1
GARBAGE_PROBABILITY = 10

# Caso tenha algum problema com a renderização da simulação, use letras no lugar de códigos unicode;
# https://www.utf8icons.com/character/9608/full-block
WALL = '\u2588'
GARBAGE = '\u2237'
HOME = 'H'
LEFT = '\u25C0'
DOWN = '\u25BC'
RIGHT = '\u25B6'
UP = '\u25B2'
EMPTY = ' '
PICK_UP = 1
DISCARD = 2

P1_COLOR = '\033[95m'
P2_COLOR = '\033[94m'
P3_COLOR = '\033[96m'
P4_COLOR = '\033[92m'
P5_COLOR = '\033[93m'
P6_COLOR = '\033[91m'
P7_COLOR = '\033[1m'
P8_COLOR = '\033[4m'
NO_COLOR = '\033[0m'

class Level:
    def __init__(self, width, height, wprob, gprob):
        self.clear()
        self.width = width
        self.height = height
        self.level = []
        self.agents = []
        for y in range(0,height):
            coll = []
            for x in range(0,width):
                if x == 0 or x == (width - 1) or y == 0 or y == (height - 1):
                    coll.append(WALL)
                elif randint(0,100) <= wprob:
                    coll.append(WALL)
                elif randint(0,100) <= gprob:
                    coll.append(GARBAGE)
                else:
                    coll.append(EMPTY)

            self.level.append(coll)


    def gotoxy(self, x, y):
        print("%c[%d;%df" % (0x1B, y, x), end='')

    def printScore(self, agent):
        self.gotoxy(1, (self.height + agent.id + 2))
        print("P1-" + str((agent.id + 1)), agent.dir, ": ", agent.score)

    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def addAgent(self, agent):
        while (True):
            x = randint(0,self.width - 1)
            y = randint(0,self.height - 1)

            if self.level[y][x] in (EMPTY, GARBAGE):
                self.level[y][x] = HOME
                agent.Start(x, y, self.level, len(self.agents))
                agent.Draw()
                break

        self.agents.append(agent);

    def run(self):
        while (True):
            for agent in self.agents:
                agent.Update()

            self.draw()
            for agent in self.agents:
                agent.Draw()
                self.printScore(agent)

            sleep(SLEEP)

    def draw(self):
        self.gotoxy(0,0)
        for y in range(0, self.height):
            for x in range(0,self.width):
                print(self.level[y][x],end="")
            print("")

class VacuumCleanerAgent:
    def __init__(self, brain, color):
        self.x = 0
        self.y = 0
        self.dir = UP
        self.color = color
        self.score = 0
        self.full = False
        self.brain = brain

    def Start(self, x, y, level, uid):
        self.x = x
        self.y = y
        self.level = level
        self.id = uid

    def Move(self, direction):
        sx = self.x
        sy = self.y

        if (direction == UP):
            sy -= 1
        elif (direction == DOWN):
            sy += 1
        elif (direction == LEFT):
            sx -= 1
        elif (direction == RIGHT):
            sx += 1
        else:
            return

        if (self.level[sy][sx] in (EMPTY, HOME, GARBAGE)):
            self.dir = self.color + direction + NO_COLOR
            self.x = sx
            self.y = sy

    def Draw(self):
        print("%c[%d;%df" % (0x1B, self.y+1, self.x+1), end='')
        print(self.dir)

    def Update(self):
        px = self.x
        py = self.y

        perception = [
            [self.level[py - 1][px - 1], self.level[py - 1][px], self.level[py - 1][px + 1]],
            [self.level[py    ][px - 1], self.level[py    ][px], self.level[py    ][px + 1]],
            [self.level[py + 1][px - 1], self.level[py + 1][px], self.level[py + 1][px + 1]]
        ]

        action = self.brain.NextAction(perception)
        if (action == PICK_UP):
            if (self.full == False and self.level[py][px] == GARBAGE):
                self.full = True
                self.level[py][px] = EMPTY
        elif (action == DISCARD):
            if (self.full == True and self.level[py][px] == HOME):
                self.full = False
                self.score += 1
        else:
            self.Move(action);

class Brain:
    def __init__(self):
        self.loaded = False

    def NextAction(self,perception):
        # Percepções é uma matrix 3x3 com os dados que estão ao redor do VaccumCleaner
        # GARBAGE, WALL, EMPTY, HOME ou outro jogador (LEFT, UP, DOWN, RIGHT)

        # Lista de ações possíveis
        # UP, DOWN, LEFT, RIGHT, PICK_UP, DISCARD
        if (perception[1][1] == GARBAGE):
            self.loaded = True
            return PICK_UP
        elif (self.loaded):
            if (perception[1][1] == HOME):
                self.loaded = False
                return DISCARD
            else:
                return DOWN
        return UP

class Brain2:
    def __init__(self):
        self.loaded = False

    def NextAction(self,perception):
        # Percepções é uma matrix 3x3 com os dados que estão ao redor do VaccumCleaner
        # GARBAGE, WALL, EMPTY, HOME ou outro jogador (LEFT, UP, DOWN, RIGHT)

        # Lista de ações possíveis
        # UP, DOWN, LEFT, RIGHT, PICK_UP, DISCARD
        if (perception[1][1] == GARBAGE):
            self.loaded = True
            return PICK_UP
        elif (self.loaded):
            if (perception[1][1] == HOME):
                self.loaded = False
                return DISCARD
            else:
                return LEFT
        return RIGHT

class Brain3:
    def __init__(self):
        from typing import List
        self.turn = 0
        self.loaded = False
        self.home = [50,50]
        self.position = [50,50]
        self.move = 0
        self.travel: List[str] = [] 
        self.regression =  False #se o algoritimo vai ficar dando pop pra voltar pra home
        self.progression = False
        self.go: List[str] = [] 
        self.rageMode = 0
        #fazer nossa matriz
        n = 100
        m = 100
        self.matriz = []
        for i in range(n):
            line = []
            for j in range(m):
                line.append('#')
            self.matriz.append(line)
        self.matriz [50][50] = 'H'
        #printar a nossa matriz
        '''
        for line in self.matriz:
            print (' '.join(map(str, line)))
        '''


    def NextAction(self,perception):
        # Percepções é uma matrix 3x3 com os dados que estão ao redor do VaccumCleaner
        # GARBAGE, WALL, EMPTY, HOME ou outro jogador (LEFT, UP, DOWN, RIGHT)

        # 0 1 2 
        # 3 4 5 
        # 6 7 8 


        # . = ja andou, # = nao descoberto, W = parede, X = LIXO, H = HOME, 0 ja viu
        # Lista de ações possíveis
        # UP, DOWN, LEFT, RIGHT, PICK_UP, DISCARD
        
        #modo regressao, pra voltar pra casa home (n sei se vai usar, depende da logica)
        if self.loaded == True:
            try:
                # Obtendo o elemento mais novo
                lastmove = self.travel.pop()  
                if lastmove == UP:
                    self.move = DOWN
                    self.go.append(UP)
                if lastmove == LEFT:
                    self.move = RIGHT
                    self.go.append(LEFT)
                if lastmove == RIGHT:
                    self.move = LEFT
                    self.go.append(RIGHT)
                if lastmove == DOWN:
                    self.move = UP
                    self.go.append(DOWN)
            except IndexError:
                self.move = DISCARD
                self.regression = False
                self.progression = True
                self.loaded = False
                return DISCARD
                

        #popular a matriz com os dados que ele coletou na perception MODO PEDREIRO
        if self.matriz[self.position[0]][self.position[1]] != 'H':
            self.matriz[self.position[0]][self.position[1]] = '.'
        if self.matriz[self.position[0]-1][self.position[1]-1] != 'H' and self.matriz[self.position[0]-1][self.position[1]-1] != '.':
            self.matriz[self.position[0]-1][self.position[1]-1] = perception[0][0]
        if self.matriz[self.position[0]][self.position[1]-1] != 'H' and self.matriz[self.position[0]][self.position[1]-1] != '.':
            self.matriz[self.position[0]][self.position[1]-1] = perception[1][0]
        if self.matriz[self.position[0]+1][self.position[1]-1] != 'H' and self.matriz[self.position[0]+1][self.position[1]-1] != '.':
            self.matriz[self.position[0]+1][self.position[1]-1] = perception[2][0]
        if self.matriz[self.position[0]-1][self.position[1]] != 'H' and self.matriz[self.position[0]-1][self.position[1]] != '.':
            self.matriz[self.position[0]-1][self.position[1]] = perception[0][1]
        if self.matriz[self.position[0]-1][self.position[1]+1] != 'H' and self.matriz[self.position[0]-1][self.position[1]+1] != '.':
            self.matriz[self.position[0]-1][self.position[1]+1] = perception[0][2]
        if self.matriz[self.position[0]][self.position[1]+1] != 'H' and self.matriz[self.position[0]][self.position[1]+1] != '.':
            self.matriz[self.position[0]][self.position[1]+1] = perception[1][2]
        if self.matriz[self.position[0]+1][self.position[1]] != 'H' and self.matriz[self.position[0]+1][self.position[1]] != '.':
            self.matriz[self.position[0]+1][self.position[1]] = perception[2][1]
        if self.matriz[self.position[0]+1][self.position[1]+1] != 'H' and self.matriz[self.position[0]+1][self.position[1]+1] != '.':
            self.matriz[self.position[0]+1][self.position[1]+1] = perception[2][2]
        
        

        #movimentacoes
        if self.loaded == False:
            self.turn += 1
            if self.turn == 15:
                self.rageMode = self.move
                self.turn = 0

            if perception[1][1] == '∷':
                for line in self.matriz:
                    print (' '.join(map(str, line)))
                self.move = PICK_UP
                self.regression = True
                self.loaded = True
            else:
                #o rand eh so pra mostrar como ta
                import random 
                pathOfTruth = random.randint(0, 3)
                if pathOfTruth==0:
                    self.move = RIGHT
                elif pathOfTruth==1:
                    self.move = LEFT
                elif pathOfTruth==2:
                    self.move = UP
                elif pathOfTruth==3:
                    self.move = DOWN
        
        if self.loaded == True and perception[1][1] == 'H':
            self.move = DISCARD
            self.loaded = False
        
        
        if self.loaded == False and self.rageMode != 0:
            if self.turn > 5:
                self.rageMode = 0
            self.move = self.rageMode
            self.turn = 0
        #fazendo movimento e mudando posicao
        if self.move == UP:
            if perception[0][1] != WALL:
                self.position[0]=self.position[0]-1
                if self.loaded == False:
                    self.travel.append(UP)         
                return UP
            else:
                self.rageMode = 0
        if self.move == LEFT:
            if perception[1][0] != WALL:
                self.position[1]=self.position[1]-1
                if self.loaded == False:
                    self.travel.append(LEFT)
                return LEFT
            else:
                self.rageMode = 0
        if self.move == DOWN:
            if perception[2][1] != WALL:
                self.position[0]=self.position[0]+1
                if self.loaded == False:
                    self.travel.append(DOWN)
                return DOWN
            else:
                self.rageMode = 0
        if self.move == RIGHT:
            if perception[1][2] != WALL:
                if self.loaded == False:
                    self.travel.append(RIGHT)
                self.position[1]=self.position[1]+1
                return RIGHT
            else:
                self.rageMode = 0
        if self.move == PICK_UP:
            return PICK_UP
        if self.move == DISCARD:
            return DISCARD


class Brain4:
    def __init__(self):
        self.loaded = False

    def NextAction(self,perception):
        # Percepções é uma matrix 3x3 com os dados que estão ao redor do VaccumCleaner
        # GARBAGE, WALL, EMPTY, HOME ou outro jogador (LEFT, UP, DOWN, RIGHT)

        # Lista de ações possíveis
        # UP, DOWN, LEFT, RIGHT, PICK_UP, DISCARD
        if (perception[1][1] == GARBAGE):
            self.loaded = True
            return PICK_UP
        elif (self.loaded):
            if (perception[1][1] == HOME):
                self.loaded = False
                return DISCARD
            else:
                return UP
        return DOWN

level = Level(LEVEL_WIDTH, LEVEL_HEIGHT, WALL_PROBABILITY, GARBAGE_PROBABILITY)
#level.addAgent(VacuumCleanerAgent(Brain(), P1_COLOR))
#level.addAgent(VacuumCleanerAgent(Brain2(), P2_COLOR))
level.addAgent(VacuumCleanerAgent(Brain3(), P3_COLOR))
#level.addAgent(VacuumCleanerAgent(Brain4(), P4_COLOR))
level.run()
