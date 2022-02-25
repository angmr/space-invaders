# Space Invaders
# python 3.9.1 on Windows
# Thanks to Christian Thompson 
# Python Game Programming Tutorial: Space Invaders
# http://christianthompson.com/
# Thanks to Pedram Badakhchani, https://github.com/pedbad

import turtle
import math
import random
import winsound
import time
from pygame import mixer

# Set up the screen
win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.bgpic("space_invaders_background.gif")
win.tracer(0)

# Register the graphics for the game
win.register_shape("invader.gif")
win.register_shape("player.gif")
win.register_shape("invader_red.gif")
win.register_shape("invader_white.gif")
win.register_shape("player_damaged.gif")
win.register_shape("music_on.gif")
win.register_shape("music_off.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Draw sound icon
sound_icon = turtle.Turtle()
sound_icon.shape("music_on.gif")
sound_icon.setposition(285, 280)

# Set the score
score = 100

# Game state
game_over = False

# Draw the score on stage
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 265)
scorestring = f"Score: {score}"
score_pen.write(scorestring, False, align="left", font=("Agency FB", 20, "bold"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.shape("player.gif")
player.speed(0)
player.penup()
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# Choose number of enemies
number_of_enemies = 4
# Create an empty list of enemies
enemiesList = []
# Add enemies to the list
# We need to create more turtle objects
for i in range(number_of_enemies):
    # Create the enemy
    enemiesList.append(turtle.Turtle())
for enemy in enemiesList:
    enemy.shape("invader.gif")
    enemy.speed(0)
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    enemy.setposition(x, y)
    enemy.enemyspeed = random.uniform(0.03, 0.1)
    enemy.type = "green"

red_enemies = []
white_enemies = []

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.speed(0)
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.goto(0, 300)
bullet.hideturtle()

bulletspeed = 1.2

# Define bullet state
# we have 2 states:
# ready - ready to fire bullet
# fire - bullet is firing

bulletstate = "ready"


# Play background music
def play_music(sound_file):
    mixer.init()
    mixer.music.load(sound_file)
    mixer.music.play(-1)


def toggle_music(x, y):
    if mixer.music.get_busy():
        mixer.music.pause()
        sound_icon.shape("music_off.gif")
    else:
        sound_icon.shape("music_on.gif")
        mixer.music.unpause()


# Move the player left and right
def move_left():
    x = player.xcor()
    x -= 10
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += 10
    if x > 280:
        x = 280

    player.setx(x)


def move_enemy(enm):
    x = enm.xcor()
    x = x + enm.enemyspeed
    enm.setx(x)

    if enm.type == "white" or enm.type == "green":
        move_amount = 40
    elif enm.type == "red":
        move_amount = 80

    if enm.xcor() > 280 or enm.xcor() < -280:
        enm.enemyspeed *= -1
        if enm.type == "green":
            for e in enemiesList:
                y = e.ycor()
                y = y - 40
                e.sety(y)
                if y <= -250:
                    y = -250
                    e.sety(y)
        y = enm.ycor()
        y -= move_amount
        enm.sety(y)
        if y <= -250:
            y = -250
            enm.sety(y)


def fire_bullet():
    global score
    # Declare bulletstate as a global if it needs change
    global bulletstate
    if bulletstate == "ready" and game_over == False:
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        score -= 1
        update_score()
        bulletstate = "fire"


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 20:
        return True
    else:
        return False


def handle_collision(blt, enm, plr):
    global bulletstate
    global score
    global game_over
    if blt:
        if enm == "red":
            winsound.PlaySound("white_spawn.wav", winsound.SND_ASYNC)
            score += 20
            spawn_white_enemies(5)
        elif enm == "green":
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            score += 10
            spawn_red_enemies(2)
        elif enm == "white":
            winsound.PlaySound("white_hit.wav", winsound.SND_ASYNC)
            score += 50

        # Reset the bullet
        bullet.hideturtle()
        bulletstate = "ready"
        bullet.setposition(0, 400)

    elif plr:
        if enm == "white":
            winsound.PlaySound("player_damage.wav", winsound.SND_ASYNC)  # sound by JoelAudio
            score -= 100
            player.shape("player_damaged.gif")
        else:
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            mixer.music.fadeout(1500)
            print("GAME OVER")
            game_over = True
            game_lost()

    update_score()


def game_lost():
    winsound.PlaySound("game_over_L.wav", winsound.SND_ASYNC)  # sound by Deathbygeko
    gameover_pen1 = turtle.Turtle()
    gameover_pen1.speed(0)
    gameover_pen1.color("white")
    gameover_pen1.penup()
    gameover_pen1.setposition(0, 10)
    gameover_string1 = "G A M E  O V E R"
    gameover_pen1.write(gameover_string1, False, align="center", font=("Felix Titling", 18, "bold"))
    gameover_pen1.hideturtle()


def update_score():
    if score < 0:
        scorestring = "Score: 0"
    else:
        scorestring = f"Score: {score}"

    score_pen.clear()
    score_pen.write(scorestring, False, align="left", font=("Agency FB", 20, "bold"))


def spawn_red_enemies(number_of_red_enemies):
    # Create red enemies
    global red_enemies
    new_reds = []
    for _ in range(number_of_red_enemies):
        new_reds.append(turtle.Turtle())

    # Set up red enemies
    for r_enemy in new_reds:
        r_enemy.shape("invader_red.gif")
        r_enemy.penup()
        r_enemy.speed(0)
        r_x = random.randint(-200, 200)
        r_y = random.randint(100, 200)
        r_enemy.setposition(r_x, r_y)
        r_enemy.enemyspeed = random.uniform(0.15, 0.2)
        r_enemy.type = "red"

    red_enemies += new_reds


def spawn_white_enemies(number_of_white_enemies):
    # Create white enemies
    global white_enemies
    new_whites = []
    for _ in range(number_of_white_enemies):
        new_whites.append(turtle.Turtle())

    # Set up white enemies
    for w_enemy in new_whites:
        w_enemy.shape("invader_white.gif")
        w_enemy.penup()
        w_enemy.speed(0)
        parent_x = r_enemy_pos[0]
        parent_y = r_enemy_pos[1]
        w_x = random.uniform(parent_x - 100, parent_x)
        w_y = random.uniform(parent_y, parent_y + 100)
        if w_x < -300:
            w_x = -100
        elif w_x > 300:
            w_x = 100
        w_enemy.setposition(w_x, w_y)
        w_enemy.enemyspeed = random.uniform(0.3, 0.4)
        w_enemy.type = "white"

    white_enemies += new_whites


win.listen()

play_music("soundtrack.wav")  # music by Mr.Kake
sound_icon.onclick(toggle_music)

# create keyboard bindings
win.onkeypress(fire_bullet, "space")
win.onkeypress(move_left, "Left")
win.onkeypress(move_right, "Right")

# --------- Main game loop ----------
while True:
    win.update()
    # Check to see if the game is over
    if not enemiesList and not red_enemies and not white_enemies:
        game_over = True
        print("GAME OVER")
        gameover_pen = turtle.Turtle()
        gameover_pen.speed(0)
        gameover_pen.color("white")
        gameover_pen.penup()
        gameover_pen.setposition(0, 0)
        gameover_string = "V I C T O R Y !\nAll invaders have been defeated."
        gameover_pen.write(gameover_string, False, align="center", font=("Felix Titling", 14, "bold"))
        gameover_pen.hideturtle()
        time.sleep(5)
        break
    for w_enemy in white_enemies:
        move_enemy(w_enemy)

        # Check for collision between bullet and white enemy
        if isCollision(bullet, w_enemy):
            w_enemy.hideturtle()
            w_enemy.goto(1000, 1000)
            white_enemies.remove(w_enemy)
            handle_collision(1, "white", 0)

        # Check for collision between white enemy and player
        if isCollision(player, w_enemy):
            w_enemy.hideturtle()
            w_enemy.goto(1000, 1000)
            white_enemies.remove(w_enemy)
            handle_collision(0, "white", 1)
            break

    for r_enemy in red_enemies:
        move_enemy(r_enemy)

        # Check for collision between bullet and red enemy
        if isCollision(bullet, r_enemy):
            r_enemy_pos = r_enemy.pos()
            handle_collision(1, "red", 0)
            red_enemies.remove(r_enemy)
            r_enemy.goto(1000, 1000)
            r_enemy.hideturtle()

        # Check for collision between red enemy and player
        if isCollision(player, r_enemy):
            player.hideturtle()
            player.goto(0, 300)
            r_enemy.hideturtle()
            handle_collision(0, "red", 1)
            break

    for enemy in enemiesList:
        move_enemy(enemy)

        # Check for collision between bullet and enemy
        if isCollision(bullet, enemy):
            handle_collision(1, "green", 0)
            enemiesList.remove(enemy)
            enemy.goto(1000, 1000)
            enemy.hideturtle()

        # Check for collision between enemy and player
        if isCollision(player, enemy):
            player.hideturtle()
            player.goto(0, 300)
            enemy.hideturtle()
            handle_collision(0, "green", 1)
            break

    # Move the bullet only when bulletstate is "fire"
    if bulletstate == "fire":
        y = bullet.ycor()
        y = y + bulletspeed
        bullet.sety(y)

    # Check to see if bullet has reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
