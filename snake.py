#!/usr/bin/env python3


import wx
import random


# Use "Space" to pause the game


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Snake1.0', size=(700, 528),
                          style=wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.panel = wx.Panel(self)

        self.square = 20

        self.timer_speed = 250

        self.level = 0
        self.lives = 3
        self.score = 0

        self.statusbar = self.CreateStatusBar(3)
        self.statusbar.SetStatusText('Score: ' + str(self.score), 0)
        self.statusbar.SetStatusText('Level: ' + str(self.level), 1)
        self.statusbar.SetStatusText('Lives: ' + str(self.lives), 2)

        self.display_width = self.GetClientSize().GetWidth() // self.square
        self.display_height = self.GetClientSize().GetHeight() // self.square

        self.start_x = self.display_width // 2
        self.start_y = self.display_height // 2

        self.x = self.start_x
        self.y = self.start_y

        self.snake = []

        self.snake_colour = '#B602AB'
        self.colour_target = '#2874F9'

        self.targets = [[0] * self.display_width for i in range(self.display_height)]
        self.target_x = 0
        self.target_y = 0

        self.paused = False

        self.Target()
        self.initSnake()

        self.timer = wx.Timer(self)
        self.timer.Start(self.timer_speed)

        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    # ............Functions...........................................

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        for row in range(self.display_height):
            for ind in range(self.display_width):
                if self.targets[row][ind] == 1:
                    self.drawRectangle(dc, ind, row, self.colour_target)
        for coord in self.snake:
            self.drawRectangle(dc, coord[0], coord[1], self.snake_colour)

    def try_to_Move(self):
        for i in range(len(self.snake)):
            st_x = self.snake[i][0]
            st_y = self.snake[i][1]
            direction = self.snake[i][2]
            new_x = st_x
            new_y = st_y

            if direction == 'right':
                new_x += 1
            elif direction == 'left':
                new_x -= 1
            elif direction == 'up':
                new_y -= 1
            elif direction == 'down':
                new_y += 1

            for coord in self.snake:
                if (new_x, new_y) == (coord[0], coord[1]):
                    return False

            if new_x < 0 or new_x > self.display_width or new_y < 0 or new_y > self.display_height:
                if new_x > self.display_width:
                    new_x -= self.display_width + 1
                elif new_x < 0:
                    new_x += self.display_width
                elif new_y > self.display_height:
                    new_y -= self.display_height + 1
                elif new_y < 0:
                    new_y += self.display_height

            self.snake[i][0] = new_x
            self.snake[i][1] = new_y

        x = self.snake[0][0]
        y = self.snake[0][1]

        if (x, y) == (self.target_x, self.target_y):
            direction = self.snake[0][2]
            if direction == 'left':
                self.snake = [[x - 1, y, direction]] + self.snake
            elif direction == 'up':
                self.snake = [[x, y - 1, direction]] + self.snake
            elif direction == 'right':
                self.snake = [[x + 1, y, direction]] + self.snake
            elif direction == 'down':
                self.snake = [[x, y + 1, direction]] + self.snake

            self.score += 1
            self.statusbar.SetStatusText('Score: ' + str(self.score), 0)
            self.clearTargets()
            self.Target()

        self.Refresh()

        a = [i[2] for i in self.snake]
        a = [self.snake[0][2]] + a
        a = a[:len(self.snake)]

        for i in range(len(self.snake)):
            self.snake[i][2] = a[i]

        return True

    def Collision(self):
        self.timer.Stop()
        self.lives -= 1
        if self.lives > 0:
            wx.MessageBox('You have - ' + str(self.lives) + ' lives left', 'You lost one life')
            self.statusbar.SetStatusText('Lives: ' + str(self.lives), 2)
            self.snake = []
            self.initSnake()
            self.clearTargets()
            self.Target()
            self.timer.Start(self.timer_speed)
            return

        dial = wx.MessageDialog(None, 'Do you wish to play again?', 'You Lost', wx.YES_NO)
        if dial.ShowModal() == wx.ID_YES:
            self.zeroGame()
            self.timer.Start(self.timer_speed)
        else:
            self.Destroy()

    def zeroGame(self):
        self.score = 0
        self.levels = 0
        self.lives = 3
        self.timer_speed = 175
        self.statusbar.SetStatusText('Score: ' + str(self.score), 0)
        self.statusbar.SetStatusText('Level: ' + str(self.level), 1)
        self.statusbar.SetStatusText('Lives: ' + str(self.lives), 2)
        self.snake = []
        self.initSnake()
        self.clearTargets()
        self.Target()

    def clearTargets(self):
        self.targets[self.target_y][self.target_x] = 0

    def Target(self):
        x = random.randint(0, self.display_width - 1)
        y = random.randint(0, self.display_height - 1)
        coords = [(row[0], row[1]) for row in self.snake]
        if (x, y) not in coords:
            self.target_x = x
            self.target_y = y
            self.targets[self.target_y][self.target_x] = 1
            self.Refresh()
        else:
            self.Target()

    def OnKeyDown(self, e):
        code = e.GetKeyCode()
        if code == 314 and self.snake[0][2] != 'right':
            self.snake[0][2] = 'left'
        elif code == 315 and self.snake[0][2] != 'down':
            self.snake[0][2] = 'up'
        elif code == 316 and self.snake[0][2] != 'left':
            self.snake[0][2] = 'right'
        elif code == 317 and self.snake[0][2] != 'up':
            self.snake[0][2] = 'down'
        elif code == wx.WXK_SPACE:
            if not self.paused:
                self.timer.Stop()
                self.paused = True
                return
            if self.paused:
                self.timer.Start(self.timer_speed)
                self.paused = False
                return
        elif code == wx.WXK_ESCAPE:
            self.Destroy()

    def OnTimer(self, e):
        if not self.try_to_Move():
            self.Collision()
        if len(self.snake) == 10:
            if self.timer_speed > 40:
                self.timer.Stop()
                self.level += 1
                self.timer_speed -= 20
                self.snake = []
                self.statusbar.SetStatusText('Level: ' + str(self.level), 1)
                wx.MessageBox('Level - ' + str(self.level), 'Achieved level up')
                self.initSnake()
                self.timer.Start(self.timer_speed)

    def initSnake(self):
        for i in range(3):
            self.snake += [[self.start_x - i, self.start_y, 'right']]

    def drawRectangle(self, dc, x, y, colour):
        dc.SetPen(wx.Pen(wx.Colour(32, 32, 32)))
        dc.SetBrush(wx.Brush(colour))
        dc.DrawRectangle(x * self.square, y * self.square, self.square, self.square)


# ------------------------------Launch the game------------------------------------------------------------


def main():
    app = wx.App()
    Frame().Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
