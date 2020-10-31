from SnakeEnvironment import SnakeEnv, Keys
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
class neural_network:
    def __init__(self):
        pass
def dir_tolist(key_press):
    output = [0,0,0,0]
    if key_press == "Down":
        output = [1,0,0,0]
    if key_press == "Up":
        output = [0,1,0,0]
    if key_press == "Left":
        output = [0,0,1,0]
    if key_press == "Right":
        output = [0,0,0,1]
    return output
def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom==0] = 1
    return x_min + nom/denom 
def dataHuman(iterations):
    SEnv = SnakeEnv()  # Creating the Snake Enviorment


    SEnv.AddSnake([255, 255, 255], [0, 255, 255])  # Snake 1
    k = Keys()
    output_data = []
    output_cache = []

    input_data =[]
    data_cache = []
    key_pressed = k.GetArrowKeyInput()
    for i in range(iterations): #Runs for 100 Frames
        output_cache.append(dir_tolist(key_pressed))
        key_pressed = k.GetArrowKeyInput()
        SEnv.Direction(0, key_pressed)  # Snake 1 Direction = Left
        
        reward = SEnv.GetReward(0)
        SEnv.NextFrame()  # Loads the NextFrame
        image = np.array(SEnv.GetFrame())  # Get the Current Frame 30x30
        # image = np.concatenate(image)
        
        image = np.dot(image[...,:3], [0.299, 0.587, 0.114])
        image.tolist()
        if reward < 0:
            data_cache = []
            output_cache = []
        if reward > 0:
            input_data += data_cache
            output_data += output_cache
            data_cache = []
            output_cache = []
        data_cache.append(image)
        time.sleep(0.1)
    
    input_data = np.array(input_data)
    output_data = np.array(output_data)
    # imx = Image.fromarray(input_data[0])
    # imx.show()

    # print(input_data.shape)
    
    # print("Input Data: " + str(input_data) + "\n")
    # print("Output Data: " + str(output_data))
    SEnv.Exit()  # Exits the Environment
    return input_data, output_data
if __name__ == "__main__":


    x = np.load("input.npy", "r")
    y = np.load("output.npy", "r")
    x = np.reshape(x, [9583, 900]) /255
    

    print(x[0])