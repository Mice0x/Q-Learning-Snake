import pygame
import random
import time
import threading
import numpy as np
from PIL import Image
from PIL import ImageDraw

class SnakeEnv():
    def __init__(self):
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.blue = (0, 0, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))

        pygame.display.set_caption('Snake')
        self.running = True
        self.food_pos = []
        self.snakes = []

        self.snake_properties = []
        self.keyboard_dir = "Down"
        self.current_direction = "Down"
        self.next_frame = False
        self.reward = 1.0
        self.data = pygame.image.tostring(self.screen, "RGB")
        gl = threading.Thread(target=self.GameLoop, args=())
        gl.start()
        
    def AddSnake(self, head_color, tail_color):
        self.snake_properties.append([head_color, tail_color, "Down"])

        x = random.randint(5, 25) * 20
        y = random.randint(5, 25) * 20
        self.snakes.append([[x, y], [x+20, y]])
    
    def GetFrame(self):
        frame = Image.frombytes("RGB", (600,600), self.data)
        frame = frame.resize((30,30))
        frame_array = np.array(frame)
        output_image = frame_array.tolist()
        return output_image
    def GetReward(self):
        pass
    def NextFrame(self):
        self.next_frame = True
    def MapBorder(self):
        border_start = 0
        border_end = 580
        border_thickness = 20

        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_end, border_thickness))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_end,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_end, border_end + border_thickness, border_thickness))
        for i, val in enumerate(self.snakes):
            HeadPosition = val[-1]

            if not border_end > HeadPosition[1] > border_thickness:
                self.SnakeDead(i)
            if not border_end > HeadPosition[0] > border_thickness:
                self.SnakeDead(i)
    
    def MoveSnakes(self):

        for i, snake in enumerate(self.snakes):
            direction = self.snake_properties[i][2]
            for index, value in enumerate(snake):
                try:
                    snake[index] = [
                        int(snake[index + 1][0]), int(snake[index + 1][1])]
                except:
                    if direction == "Down":
                        snake[index][1] += 20
                    if direction == "Up":
                        snake[index][1] -= 20
                    if direction == "Left":
                        snake[index][0] -= 20
                    if direction == "Right":
                        snake[index][0] += 20
            self.current_direction = direction

    def DrawSnakes(self):
        for i, val in enumerate(self.snakes):
            snake = val
            tail_color = self.snake_properties[i][1]
            head_color = self.snake_properties[i][0]
            for index, value in enumerate(snake):
                try:
                    next_value = snake[index + 1]
                    if next_value[0] > value[0]:
                        pygame.draw.rect(self.screen, tail_color,
                                        (value[0] + 2, value[1] + 2, 20, 16))
                    elif next_value[0] < value[0]:
                        pygame.draw.rect(self.screen, tail_color,
                                        (value[0] - 2, value[1] + 2, 20, 16))
                    elif next_value[1] > value[1]:
                        pygame.draw.rect(self.screen, tail_color,
                                        (value[0] + 2, value[1] + 2, 16, 20))
                    elif next_value[1] < value[1]:
                        pygame.draw.rect(self.screen, tail_color,
                                        (value[0] + 2, value[1] - 2, 16, 20))
                except:
                    pygame.draw.rect(self.screen, head_color,
                                    (value[0]  + 2, value[1] +2, 16, 16))

    def GameLoop(self):
        # fps = 10
        # frametime = 1/fps
        # t = time.time()
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.next_frame:
                self.next_frame = False
            # if time.time() - t >= frametime:
                self.screen.fill((0, 0, 0))

                self.MapBorder()

                self.DrawSnakes()
                self.MoveSnakes()
                self.data = pygame.image.tostring(self.screen, "RGB")

                pygame.display.flip()
                # t = time.time()

    def SnakeDead(self, snake_index):
        pass
        # self.snakes[snake_index] = random.randint(5, 25) * 20

    def Direction(self, snake_index, direction):

        self.snake_properties[snake_index][2] = direction
    def Food(self):
        pass


class Snake():
    """
    Single/MultiPlayer Snake
    """

    def __init__(self):
        super().__init__()

        self.yellow = (255, 255, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.magenta = (255, 0, 255)
        self.cyan = (0, 255, 255)
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))

        pygame.display.set_caption('Snake')

        self.snake = [[300, 300], [300, 320]]
        self.running = True
        self.food_pos = []
        self.direction = "Up"
        self.current_direction = self.direction

        self.enemy_snake = []

        self.GameLoop()

    def KeyPressed(self):
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP] and self.current_direction != "Down":
            self.direction = "Up"
        elif key_input[pygame.K_DOWN] and self.current_direction != "Up":
            self.direction = "Down"
        elif key_input[pygame.K_RIGHT] and self.current_direction != "Left":
            self.direction = "Right"
        elif key_input[pygame.K_LEFT] and self.current_direction != "Right":
            self.direction = "Left"

    def GameLoop(self):
        fps = 10
        frametime = 1/fps
        t = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.KeyPressed()
            if time.time() - t >= frametime:

                self.screen.fill((0, 0, 0))
                self.HeadPosition = self.snake[-1]
                self.MoveSnake()
                self.MapBorder()

                self.DrawSnake(self.snake, self.blue, self.yellow)

                self.Food()
                self.GetTailHit()

                pygame.display.flip()
                t = time.time()

    def DrawSnake(self, snake, head_color, tail_color):
        for index, value in enumerate(snake):
            try:
                next_value = snake[index + 1]
                if next_value[0] > value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 8, value[1] - 8, 20, 16))
                elif next_value[0] < value[0]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 12, value[1] - 8, 20, 16))
                elif next_value[1] > value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 8, value[1] - 8, 16, 20))
                elif next_value[1] < value[1]:
                    pygame.draw.rect(self.screen, tail_color,
                                     (value[0] - 8, value[1] - 12, 16, 20))
            except:
                pygame.draw.rect(self.screen, head_color,
                                 (value[0] - 8, value[1] - 8, 16, 16))

    def SnakeDead(self):
        self.snake = [[300, 300], [320, 300]]

    def MapBorder(self):
        border_start = 0
        border_end = 580
        border_thickness = 20

        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_end, border_thickness))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_end,
                                                   border_start, border_thickness, border_end))
        pygame.draw.rect(self.screen, self.green, (border_start,
                                                   border_end, border_end + border_thickness, border_thickness))

        if not border_end > self.HeadPosition[1] > border_thickness:
            self.SnakeDead()
        if not border_end > self.HeadPosition[0] > border_thickness:
            self.SnakeDead()

    def MoveSnake(self):

        for index, value in enumerate(self.snake):
            try:
                self.snake[index] = [
                    int(self.snake[index + 1][0]), int(self.snake[index + 1][1])]
            except:
                if self.direction == "Down":
                    self.snake[index][1] += 20
                if self.direction == "Up":
                    self.snake[index][1] -= 20
                if self.direction == "Left":
                    self.snake[index][0] -= 20
                if self.direction == "Right":
                    self.snake[index][0] += 20
        self.current_direction = self.direction

    def Food(self):

        while not self.food_pos:
            x = random.randint(2, 28) * 20
            y = random.randint(2, 28) * 20
            if not [x, y] in self.snake:
                self.food_pos = [x, y]
        pygame.draw.rect(self.screen, self.red,
                         (self.food_pos[0] - 8, self.food_pos[1] - 8, 16, 16))

        if self.HeadPosition == self.food_pos:
            self.food_pos = []
            self.snake.insert(0, self.snake[0])

    def GetTailHit(self):
        if self.HeadPosition in self.snake[:-1] or self.HeadPosition in self.enemy_snake:
            self.SnakeDead()





if __name__ == "__main__":

    se = SnakeEnv() #Creating the Snake Enviorment

    se.AddSnake([255, 255, 0], [255, 0, 255]) #Snake 0
    se.AddSnake([0, 255, 0], [0, 255, 255]) #Snake 1

    

    for i in range(1):
        se.Direction(0, "Left")
        se.NextFrame()
        Image = se.GetFrame()
        time.sleep(0.4)
        