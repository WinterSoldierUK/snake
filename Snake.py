import tkinter
import random

ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

WINDOW_WIDTH = COLUMNS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

window_width = canvas.winfo_width()
window_height = canvas.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#find centre of screen
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
score = 0

#Set direction of snake - note the and statements stop you from doubling back on yourself
def changeDirection(event):
    global velocityX, velocityY
    if (event.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (event.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (event.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (event.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, score

    #does the snake hit food?
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLUMNS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    #set snakes new position based on velocity
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake
    #update the snake position
    move()

    #blank out the screen
    canvas.delete("all")

    #redraw the snake head and food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    #redraw snake body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")
    
    #redraw score
    canvas.create_text(50, 10, text=f"Score: {score}", fill="white", font=("Arial", 16))

    #running at 10fps
    window.after(100, draw)

#update the screen
draw()

#check for key strokes
window.bind("<KeyRelease>", changeDirection)
window.mainloop()
