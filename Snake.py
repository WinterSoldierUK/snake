import tkinter
import random
import pygame
import sys
import json

pygame.mixer.init()
eat_sound = pygame.mixer.Sound('eating.mp3')
death_sound = pygame.mixer.Sound('aww.mp3')
wall_death_sound = pygame.mixer.Sound('explosion.mp3')

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

def randomRow():
    return random.randint(0, ROWS - 1)*TILE_SIZE

def randomColumn():
    return random.randint(0, COLUMNS - 1)*TILE_SIZE


#Set direction of snake - note the and statements stop you from doubling back on yourself
def changeDirection(event):
    global velocityX, velocityY, game_over
    if (game_over):
        if (event.keysym == "r"):
            restart()
            draw()
        elif (event.keysym == "Escape"):
            sys.exit()
        else:
            return    
    #volume
    if (event.keysym == "equal"):
        pygame.mixer.music.set_volume(1.0)
    elif (event.keysym == "minus"):
        pygame.mixer.music.set_volume(0.25) 
    
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
    elif (event.keysym == "Escape"):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        sys.exit()

def restart():
    global snake, food, snake_body, score, game_over, velocityX, velocityY
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(randomColumn(), randomRow())
    snake_body = []
    velocityX = 0
    velocityY = 0
    score = 0
    game_over = False
    pygame.mixer.music.play(loops=-1, fade_ms=2000)

def move():
    global snake, score, high_score, food, snake_body, game_over
    if (game_over):
        return
    
    #does the snake leave the screen?
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        wall_death_sound.play()
        game_over = True
        return
    
    #does the snake eat itself?
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            death_sound.play()
            game_over = True
            return

    #does the snake hit food?
    if (snake.x == food.x and snake.y == food.y):
        eat_sound.play()
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLUMNS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1
        #has a new high score been set?
        if (score > high_score):
            high_score = score
    
    #update body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            tile.x = snake_body[i - 1].x
            tile.y = snake_body[i - 1].y


    #set snakes new position based on velocity
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, game_over, score
    #update the snake position
    move()

    #blank out the screen
    canvas.delete("all")

    #redraw the snake head and food
    canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="blue")
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    #redraw snake body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")
    
    #redraw score
    if (game_over):
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text=f"Game Over!", fill="white", font=("Arial", 24))
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, text=f"Score: {score}", fill="white", font=("Arial", 24))
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60, text=f"R to Restart", fill="white", font=("Arial", 24))
        pygame.mixer.music.stop()

        if (score < high_score):
            canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100, text=f"You Failed To Beat {hero_name}!", fill="white", font=("Arial", 24))
        else:
            canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100, text=f" New High Score: {high_score}!", fill="white", font=("Arial", 24))
            save_score()

        return
    else:
        canvas.create_text(100, 10, text=f"Score: {score} High Score {high_score}", fill="white", font=("Arial", 16))

    #running at 10fps
    window.after(100, draw)

def load_score():
        global high_score, hero_name

        try:
            with open("hero.json") as f:
                hero = json.load(f)
        except FileNotFoundError:
            print('High Score File Missing - Using Defaults')
        else:
            high_score = hero["high_score"]
            hero_name = hero["hero_name"]

def save_score():
    global high_score, hero_name
    hero = { "high_score": high_score, "hero_name": hero_name } 
    with open("hero.json", "w") as f:
        json.dump(hero, f)

#initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
food = Tile(randomColumn(), randomRow())
snake_body = []
velocityX = 0
velocityY = 0
score = 0
game_over = False
#these are defaults in case the file isn't found
high_score = 5
hero_name = "Matt"
load_score()

pygame.mixer.music.load('chiptune-medium-boss.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1, fade_ms=2000)

#update the screen
draw()
#check for key strokes
window.bind("<KeyRelease>", changeDirection)
window.mainloop()
