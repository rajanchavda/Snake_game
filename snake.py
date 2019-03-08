import tkinter as tk
import queue
import random
from playsound import playsound
import threading


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.after(1, lambda: self.root.focus_force())
        self.root.title('Snake')
        self.root.configure(background="black")
        self.root.resizable(0, 0)
        self.height, self.width = 500, 500
        self.endLable = 0
        self.create_canvas()
        self.root.mainloop()

    def create_canvas(self):
        if self.endLable:
            self.scoreLabel.destroy()
            self.endLable.destroy()
            self.createdBy.destroy()

        self.canvasScore = tk.IntVar(self.root)
        self.scoreLabelCanvas = tk.Label(
            self.root, pady=4, font="Times 16 italic bold", bg="black", fg="white", textvariable=self.canvasScore)
        self.scoreLabelCanvas.pack()

        self.Points = [[220, 200], [190, 200], [200, 200], [210, 200]]
        self.First = self.Points[1]
        self.Direction = 'RIGHT'
        self.StartPos = 0
        self.EndPos = 1
        self.speed = 50
        self.mouse = [0, 0]
        self.score = 0
        self.generateMouse()

        self.c = tk.Canvas(self.root, height=self.height,
                           width=self.width, bg='black')
        self.c.pack(fill=tk.BOTH, expand=True)

        self.c.bind('<Right>', self.rightKey)
        self.c.bind('<Up>', self.upKey)
        self.c.bind('<Left>', self.leftKey)
        self.c.bind('<Down>', self.downKey)
        self.root.bind('<Escape>', self.exitGame)
        self.root.bind('<space>', self.resume)
        self.c.bind('w', self.speedDown)
        self.c.bind('e', self.speedUp)
        self.c.focus_set()

        self.runSnake()

    def create_dialogue_box(self):
        self.scoreLabelCanvas.destroy()
        score = tk.IntVar(self.root)
        score.set(self.score)
        self.scoreLabel = tk.Label(
            self.root, padx=20, pady=20, font="Times 20 italic bold",  bg="black", fg="white", textvariable=score)
        self.endLable = tk.Label(
            self.root, padx=50, pady=30, font="Times 16  bold",  bg="black", fg="white", text="Try one more time Kido.\n\n Press <Space> for New Game.\nPress <Esc> to exit.")
        self.createdBy = tk.Label(
            self.root, padx=20, pady=5, font="Times 12 italic",  bg="black", fg="white", text='Created by Rajan')

        self.scoreLabel.pack()
        self.endLable.pack()
        self.createdBy.pack()

    def play_sound(self):
        playsound('./Sounds/AWM_Shot.mp3')

    def updateScore(self):
        self.score += 1

    def speedUp(self, _event=None):
        self.speed -= 10

    def speedDown(self, _event=None):
        self.speed += 10

    def resume(self, _event=None):
        self.create_canvas()

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

    def stopGame(self, _event=None):
        self.c.destroy()
        self.create_dialogue_box()

    def isSnakeCollide(self):
        self.newL = []
        self.newL = self.Points.copy()
        old_start_point = self.Points[self.StartPos]
        self.newL.remove(self.Points[self.StartPos])

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
        self.updateScore()
        self.canvasScore.set(self.score)

    def generateMouse(self):
        x, y = random.randrange(0, 490, 10), random.randrange(0, 490, 10)
        if [x, y] in self.Points:
            self.generateMouse()
        else:
            self.mouse = [x, y]

    def removeLast(self, leftright, updown):
        if self.Points[self.StartPos] == self.mouse:
            self.updatePoints(
                [self.mouse[0]+leftright, self.mouse[1]+updown])
            thread1 = threading.Thread(target=self.play_sound)
            thread1.start()
            self.generateMouse()
        else:
            self.Points[self.EndPos] = [self.Points[self.StartPos]
                                        [0]+leftright, self.Points[self.StartPos][1]+updown]

    def changeLastPoint(self):
        if self.Direction == 'RIGHT':
            self.removeLast(10, 0)

        elif self.Direction == 'DOWN':
            self.removeLast(0, 10)

        elif self.Direction == 'LEFT':
            self.removeLast(-10, 0)

        elif self.Direction == 'UP':
            self.removeLast(0, -10)

    def drawSnake(self):

        self.c.delete("all")
        self.makeSolidBox(self.c, self.mouse[0], self.mouse[1], 'yellow')
        for i in self.Points:
            if self.Points.index(i) == self.StartPos:
                self.makeSolidBox(self.c, i[0], i[1], 'white')
            else:
                self.makeSolidBox(self.c, i[0], i[1], 'red')

        self.changeLastPoint()
        self.roll()
        if self.isSnakeCollide():
            self.stopGame()

    def runSnake(self):
        # print(self.StartPos)
        if (self.Points[self.StartPos][0] < self.height and self.Points[self.StartPos][1] < self.width) and (self.Points[self.StartPos][0] >= 0 and self.Points[self.StartPos][1] >= 0):

            self.drawSnake()
            # print(self.Points)
            self.root.after(self.speed, self.runSnake)
        else:
            self.stopGame()


app = App()
