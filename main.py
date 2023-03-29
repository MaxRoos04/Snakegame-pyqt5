import sys
import random
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget


class Snake(QWidget):
    def __init__(self):
        super().__init__()

        self.score = 0
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Snake')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)

        self.direction = 'Right'

        self.food = self.create_food()

        self.snake = [(200, 150), (190, 150), (180, 150)]

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_background(qp)
        self.draw_snake(qp)
        self.draw_food(qp)
        self.draw_score(qp)
        qp.end()
    
    def draw_background(self, qp):
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(QRect(0, 0, self.width(), self.height()))

    def draw_snake(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 255, 0))
        for pos in self.snake:
            qp.drawRect(QRect(pos[0], pos[1], 10, 10))

    def draw_food(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(QRect(self.food[0], self.food[1], 10, 10))
    
    def draw_score(self, qp):
        qp.setPen(QColor(125, 125, 125))
        qp.setFont(QFont('Arial', 10))
        qp.drawText(QPoint(10, 20), 'Score: {}'.format(self.score))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right and self.direction != 'Left':
            self.direction = 'Right'
        elif event.key() == Qt.Key_Left and self.direction != 'Right':
            self.direction = 'Left'
        elif event.key() == Qt.Key_Up and self.direction != 'Down':
            self.direction = 'Up'
        elif event.key() == Qt.Key_Down and self.direction != 'Up':
            self.direction = 'Down'

    def move_snake(self):
        if self.direction == 'Right':
            self.snake.insert(0, (self.snake[0][0] + 10, self.snake[0][1]))
        elif self.direction == 'Left':
            self.snake.insert(0, (self.snake[0][0] - 10, self.snake[0][1]))
        elif self.direction == 'Up':
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - 10))
        elif self.direction == 'Down':
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + 10))

        if self.snake[0][0] == self.food[0] and self.snake[0][1] == self.food[1]:
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.check_collision()

        self.update()

    def create_food(self):
        x = round((random.randrange(0, 390) / 10)) * 10
        y = round((random.randrange(0, 290) / 10)) * 10

        self.score += 10
        
        return (x, y)

    def check_collision(self):
        if self.snake[0][0] < 0 or self.snake[0][0] > 390 or self.snake[0][1] < 0 or self.snake[0][1] > 290:
           self.timer.stop()
           self.game_over()

        for i in range(1, len(self.snake)):
           if self.snake[0][0] == self.snake[i][0] and self.snake[0][1] == self.snake[i][1]:
              self.timer.stop()
              self.game_over()

    def game_over(self):
        print('Game over')

if __name__ == '__main__':
     app = QApplication(sys.argv)
     snake = Snake()
     sys.exit(app.exec_())

