import pygame
import random
import time
import threading
import numpy as np
from PIL import Image


class SnakeEnv():
    def __init__(self):
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
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
        self.gl = threading.Thread(target=self.GameLoop, args=())
        self.gl.start()

    def spawnPos(self):
        not_in_other_snake = False
        x = 0
        y = 0
        while True:
            if not_in_other_snake:
                not_in_other_snake = False
                break
            x = random.randint(1, 27) * 20
            y = random.randint(1, 28) * 20
            if not self.snakes:
                not_in_other_snake = True
            for i, snake in enumerate(self.snakes):

                if not [x, y] in snake and not [x+20, y] in snake and not [x+20, y] in self.food_pos:
                    if i + 1 == len(self.snakes):
                        not_in_other_snake = True
                else:
                    not_in_other_snake = False
                    break
        return [[x, y], [x+20, y]]

    def AddSnake(self, head_color, tail_color):
        self.snake_properties.append([head_color, tail_color, "Down", 0.0])

        self.snakes.append(self.spawnPos())

    def Exit(self):
        self.running = False
        self.gl.join()

    def GetFrame(self):
        frame = Image.frombytes("RGB", (600, 600), self.data)
        frame = frame.resize((30, 30))
        frame_array = np.array(frame)
        output_image = frame_array.tolist()
        return output_image

    def GetReward(self, snake_index):
        return self.snake_properties[snake_index][3]
    def AddReward(self, snake_index, reward):
        self.snake_properties[snake_index][3] = reward
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
        for i, snake in enumerate(self.snakes):
            HeadPosition = snake[-1]

            if not border_end > HeadPosition[1] > border_thickness:
                self.AddReward(i, -1.0)
                self.SnakeDead(i)
            if not border_end > HeadPosition[0] > border_thickness:
                self.AddReward(i, -1.0)
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
                                     (value[0] + 2, value[1] + 2, 16, 16))

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
                for index, val in enumerate(self.snake_properties):
                    self.AddReward(index, 0.0)
                self.MapBorder()

                self.DrawSnakes()
                self.MoveSnakes()
                self.Food()
                self.TailHit()
                self.data = pygame.image.tostring(self.screen, "RGB")

                pygame.display.flip()
                # t = time.time()

    def SnakeDead(self, snake_index):
        self.snakes[snake_index] = self.spawnPos()

    def Direction(self, snake_index, direction):
        if self.snake_properties[snake_index][2] == "Up" and direction != "Down":
            self.snake_properties[snake_index][2] = direction
        elif self.snake_properties[snake_index][2] == "Down" and direction != "Up":
            self.snake_properties[snake_index][2] = direction
        elif self.snake_properties[snake_index][2] == "Left" and direction != "Right":
            self.snake_properties[snake_index][2] = direction
        elif self.snake_properties[snake_index][2] == "Right" and direction != "Left":
            self.snake_properties[snake_index][2] = direction

    def Food(self):

        for index, snake in enumerate(self.snakes):
            HeadPosition = snake[-1]
            if HeadPosition == self.food_pos:
                self.AddReward(index, 1.0)
                self.food_pos = []
                self.snakes[index].insert(0, self.snakes[index][0])
        if not self.food_pos:
            self.food_pos = self.spawnPos()[0]
        pygame.draw.rect(self.screen, self.red,
                         (self.food_pos[0] + 2, self.food_pos[1] + 2, 16, 16))

    def TailHit(self):
        for index, snake in enumerate(self.snakes):
            HeadPosition = snake[-1]
            if HeadPosition in snake[:-1]:
                self.SnakeDead(index)
                self.AddReward(index, -1.0)
            for i,s in enumerate(self.snakes):
                if i != index:
                    if HeadPosition in s:
                        self.AddReward(i,2.0)
                        self.AddReward(index, -1.0)
                        self.SnakeDead(index)
                        

if __name__ == "__main__":

    SEnv = SnakeEnv()  # Creating the Snake Enviorment

    SEnv.AddSnake([255, 255, 0], [255, 0, 255])  # Snake 0
    for i in range(100):
        SEnv.AddSnake([0, 255, 0], [0, 255, 255])  # Snake 1
    move = "Up"
    for i in range(10000):

        SEnv.Direction(1, "Left")
        SEnv.Direction(0, "Right")
        print(SEnv.GetReward(0))
        SEnv.NextFrame()
        image = SEnv.GetFrame()
        time.sleep(2)
    SEnv.Exit()
