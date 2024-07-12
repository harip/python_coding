import pgzrun
from pgzero.actor import Actor
from random import randint

WIDTH = 700
HEIGHT = 600
fox_score = 0
hedgehog_score = 0
game_over = False
player_speed = 10
scores = []
high_score_run = True
time_left = 60

fox = Actor("fox")
fox.pos = 100, 100
hedgehog = Actor("hedgehog")
hedgehog.pos = 400, 400
coin = Actor("coin")
coin.pos = 200, 200

def draw():
    global game_over, high_score_run

    if not game_over:
        screen.fill("green")
        fox.draw()
        coin.draw()
        hedgehog.draw()
        screen.draw.text("Fox score: " + str(fox_score), color="black", topleft =(10, 10))
        screen.draw.text("Hedgehog score: " + str(hedgehog_score), color="black", topleft =(10, 30))
        screen.draw.text(str(time_left), color=("Black"), topright =(700, 0), fontsize= 50)

    if game_over:
        screen.clear()
        screen.fill("green")
        screen.draw.text("Fox Score: " + str(fox_score), color= "black", topleft = (10, 10), fontsize = 30)
        screen.draw.text("Hedgehog Score: " + str(hedgehog_score), color= "black", topleft = (10, 30), fontsize = 30)
        if high_score_run == True:
            update_high_scores()
            # display_high_scores()
        high_score_run = False
        display_high_scores()

def place_coin():
    coin.x = randint(20, (WIDTH - 20))
    coin.y = randint(20, (HEIGHT - 20))

def time_up():
    global game_over
    game_over = True

def update_time_left():
    global time_left

    if time_left:
        time_left -= 1
    else:
        time_up()

def update_high_scores():
    global fox_score, hedgehog_score, fox_scores, hedgehog_scores, high_scores

    filename = r"C:\\Users\\igres\\Desktop\boy\\pygame_game\\coin_collector\\fox_high_scores.txt"
    fox_scores = []
    with open(filename, "r") as file:
        line = file.readline()
        fox_scores = line.split()
        fox_scores.insert(0, fox_score)    
    with open(filename, "w") as file:
        for high_score in fox_scores:
            file.write(str(high_score) + " ")

    filename = r"C:\\Users\\igres\\Desktop\boy\\pygame_game\\coin_collector\\hedgehog_high_scores.txt"
    hedgehog_scores = []
    with open(filename, "r") as file:
        line = file.readline()
        hedgehog_scores = line.split()
        hedgehog_scores.append(str(hedgehog_score) + " ")
    with open(filename, "w") as file:
        for high_score in hedgehog_scores:
            file.write(str(high_score) + " ")

def display_high_scores():
    all_high_scores = fox_scores+hedgehog_scores
    all_high_scores = list(map(int, all_high_scores))
    all_high_scores.sort(reverse=True)
    screen.draw.text("High Scores", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in all_high_scores:
        screen.draw.text(str(position) + ". " + str(high_score), (350, y), color="black")
        y += 25
        position += 1

def update():
    global hedgehog_score, fox_score

    if fox.x > 20:
        if keyboard.left:
            fox.x -= player_speed
    if fox.x < (WIDTH -20):
        if keyboard.right:
            fox.x += player_speed
    if fox.y > 20:
        if keyboard.up:
            fox.y -= player_speed
    if fox.y < (HEIGHT -20):
        if keyboard.down:
            fox.y += player_speed

    if hedgehog.x > 20:
        if keyboard.a:
            hedgehog.x -= player_speed
    if hedgehog.x < (WIDTH -20):
        if keyboard.d:
            hedgehog.x += player_speed
    if hedgehog.y > 20:
        if keyboard.w:
            hedgehog.y -= player_speed
    if hedgehog.y < (HEIGHT -20):
        if keyboard.s:
            hedgehog.y += player_speed


    fox_coin_collected = fox.colliderect(coin)
    hedgehog_coin_collected = hedgehog.colliderect(coin)

    if fox_coin_collected:
        fox_score += 10
        place_coin()
    
    if hedgehog_coin_collected:
        hedgehog_score += 10
        place_coin()

clock.schedule_interval(update_time_left, 1.0)
place_coin()

pgzrun.go()