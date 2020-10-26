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
        frame = Image.frombytes("RGB", (600, 600), self.data)
        frame = frame.resize((30, 30))
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


if __name__ == "__main__":

    se = SnakeEnv()  # Creating the Snake Enviorment

    se.AddSnake([255, 255, 0], [255, 0, 255])  # Snake 0
    se.AddSnake([0, 255, 0], [0, 255, 255])  # Snake 1

    for i in range(1):
        se.Direction(0, "Left")
        se.NextFrame()
        Image = se.GetFrame()
        time.sleep(0.4)
