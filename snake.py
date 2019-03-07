import tkinter as tk
import queue
import random


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.after(1, lambda: self.root.focus_force())
        self.root.resizable(0, 0)
        self.height, self.width = 500, 500
        self.c = tk.Canvas(self.root, height=500, width=500, bg='black')
        self.c.pack(fill=tk.BOTH, expand=True)
        self.startX, self.startY = 200, 200

        self.Points = [[220, 200], [190, 200], [200, 200], [210, 200]]
        self.First = self.Points[1]
        self.Direction = 'RIGHT'
        self.StartPos = 0
        self.EndPos = 1
        self.speed = 50
        self.mouse = [330, 200]

        # widget = self.c.create_text(0, 0, fill="white", anchor="nw", font="Times 10 italic bold",
        #                             text="Click the bubbles that are multiples of two.")

        # self.c.bind('<Configure>', self.create_grid)
        self.c.bind('<Right>', self.rightKey)
        self.c.bind('<Up>', self.upKey)
        self.c.bind('<Left>', self.leftKey)
        self.c.bind('<Down>', self.downKey)
        self.c.bind('<Escape>', self.exitGame)
        self.c.bind('<space>', self.resume)
        self.c.bind('w', self.speedDown)
        self.c.bind('e', self.speedUp)
        self.c.focus_set()

        self.runSnake()
        self.root.mainloop()

    # def create_canvas(self):

    def speedUp(self, _event=None):
        self.speed -= 10

    def speedDown(self, _event=None):
        self.speed += 10

    def resume(self, _event=None):
        self.speed = 50

    def rightKey(self, _event=None):
        if self.Direction != 'LEFT':
            self.Direction = 'RIGHT'

    def upKey(self, _event=None):
        if self.Direction != 'DOWN':
            self.Direction = 'UP'

    def downKey(self, _event=None):
        if self.Direction != 'UP':
            self.Direction = 'DOWN'

    def leftKey(self, _event=None):
        if self.Direction != 'RIGHT':
            self.Direction = 'LEFT'

    def exitGame(self, _event=None):
        self.root.destroy()
        exit()

    def newGame(self, _event=None):
        # self.speed = 1000*60*60
        self.root.destroy()
        App()

    def isSnakeCollide(self):
        self.newL = []
        self.newL = self.Points.copy()
        old_start_point = self.Points[self.StartPos]
        self.newL.remove(self.Points[self.StartPos])
        # print(self.newL)
        if old_start_point in self.newL:
            return True
        else:
            return False

    def makeSolidBox(self, c, x1, y1, color):
        return self.c.create_rectangle(
            x1, y1, x1+10, y1+10, width=0, fill=color)

    def roll(self):
        if self.StartPos < (len(self.Points)-2):
            self.StartPos += 1
            self.EndPos += 1
        elif self.StartPos == (len(self.Points)-2):
            self.StartPos += 1
            self.EndPos = 0
        elif self.StartPos == (len(self.Points)-1):
            self.StartPos = 0
            self.EndPos = 1

    def updatePoints(self, newPoint):
        newList = self.Points[:self.StartPos + 1] + \
            [newPoint] + self.Points[self.StartPos+1:]
        self.Points = newList

    def generateMouse(self):
        x, y = random.randrange(0, 490, 10), random.randrange(0, 490, 10)
        if [x, y] in self.Points:
            self.generateMouse()
        else:
            self.mouse = [x, y]

    def changeLastPoint(self):
        # print(self.Points)
        if self.Direction == 'RIGHT':
            if self.Points[self.StartPos] == self.mouse:
                self.updatePoints([self.mouse[0]+10, self.mouse[1]])
                self.generateMouse()
                # print(len(self.Points))
            else:
                self.Points[self.EndPos] = [self.Points[self.StartPos]
                                            [0]+10, self.Points[self.StartPos][1]]

        elif self.Direction == 'DOWN':
            if self.Points[self.StartPos] == self.mouse:
                self.updatePoints([self.mouse[0], self.mouse[1]+10])
                self.generateMouse()
                # print(len(self.Points))
            else:
                self.Points[self.EndPos] = [self.Points[self.StartPos]
                                            [0], self.Points[self.StartPos][1]+10]

        elif self.Direction == 'LEFT':
            if self.Points[self.StartPos] == self.mouse:
                self.updatePoints([self.mouse[0]-10, self.mouse[1]])
                self.generateMouse()
                # print(len(self.Points))
            else:
                self.Points[self.EndPos] = [self.Points[self.StartPos]
                                            [0]-10, self.Points[self.StartPos][1]]

        elif self.Direction == 'UP':
            if self.Points[self.StartPos] == self.mouse:
                self.updatePoints([self.mouse[0], self.mouse[1]-10])
                self.generateMouse()
                # print(len(self.Points))
            else:
                self.Points[self.EndPos] = [self.Points[self.StartPos]
                                            [0], self.Points[self.StartPos][1]-10]

    def drawSnake(self):

        self.c.delete("all")
        self.makeSolidBox(self.c, self.mouse[0], self.mouse[1], 'yellow')
        for i in self.Points:
            if self.Points.index(i) == self.StartPos:
                self.makeSolidBox(self.c, i[0], i[1], 'white')
            # elif self.Points.index(i) == self.EndPos:
            #     self.makeSolidBox(self.c, i[0], i[1], 'green')
            else:
                self.makeSolidBox(self.c, i[0], i[1], 'red')

        self.changeLastPoint()
        self.roll()
        if self.isSnakeCollide():
            self.newGame()

    def runSnake(self):
        # print(self.StartPos)
        if (self.Points[self.StartPos][0] < 500 and self.Points[self.StartPos][1] < 500) and (self.Points[self.StartPos][0] >= 0 and self.Points[self.StartPos][1] >= 0):

            self.drawSnake()
            # print(self.Points)
            self.root.after(self.speed, self.runSnake)
        else:
            self.newGame()
    # def create_grid(self, event=None):
    #     self.w = self.c.winfo_width()  # Get current width of canvas
    #     self.h = self.c.winfo_height()  # Get current height of canvas
    #     self.c.delete('grid_line')  # Will only remove the grid_line


app = App()
