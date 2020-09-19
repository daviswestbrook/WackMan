# Davis Westbrook

# This code utilizes gamebox.py, an auxiliary program authored by Luther Tychonievich

# Wackman is a PacMan-like game
# the goal is to collect as many dots without getting eaten
# by one of the five sneaky cobras
# The user uses the arrow keys to move around within the walls and avoid enemies

# The game includes:
# Animation: for wackman and cobras
# Enemies: "kill" the player and end the game immediately if in contact with player
# Collectibles: goal of the game is to collect as many bloops as possible
# Intersession Progress: in the form of a running high score file

# Additionally, the color scheme changes after every "level",
# when all the bloops are consumed and subsequently replenished


import pygame
import gamebox


################ SCENERY AND GAME SPECS ###################
width = 800
height = 600

camera = gamebox.Camera(width, height)

title_color = 'white'
background_color = 'light blue'
wall_color = 'black'
scoreboard_color = 'black'
stats_text_color = 'white'
bloop_color = 'white'
start_color = 'white'
dead_color = 'red'
wackman_speed = 10
cobra_speed = 10

w = width/50
h = height/40

W = gamebox.from_text(7*w, h, "W", 50, title_color)
A1 = gamebox.from_text(13*w, h, "A", 50, title_color)
C = gamebox.from_text(19*w, h, "C", 50, title_color)
K = gamebox.from_text(25*w, h, "K", 50, title_color)
M = gamebox.from_text(31*w, h, "M", 50, title_color)
A2 = gamebox.from_text(37*w, h, "A", 50, title_color)
N = gamebox.from_text(43*w, h, "N", 50, title_color)


def draw_title():
    '''
    draws the title at top
    :return: none
    '''
    camera.draw(W)
    camera.draw(A1)
    camera.draw(C)
    camera.draw(K)
    camera.draw(M)
    camera.draw(A2)
    camera.draw(N)


def draw_start_text():
    '''
    draws text at start screen
    :return: none
    '''
    start_title = gamebox.from_text(25*w, 5*h, "WACKMAN", 50, start_color)
    start_names = gamebox.from_text(25*w, 15*h, "CREATED BY: DAVIS WESTBROOK", 35, start_color)
    start_instructions = gamebox.from_text(25*w, 25*h, "USE ARROWS TO MOVE", 25, start_color)
    press_space = gamebox.from_text(25*w, 35*h, "PRESS SPACE TO START", 25, start_color)
    camera.draw(start_title)
    camera.draw(start_names)
    camera.draw(start_instructions)
    camera.draw(press_space)


def handle_high_score():
    global high_score
    stream = open('highscore.py')
    high_score = stream.read()
    if score > int(high_score):
        with open('highscore.py', 'w') as f:
            f.write(str(score))


def draw_dead_text():
    '''
    draws text at dead screen
    :return: none
    '''
    you_died = gamebox.from_text(25*w, 15*h, "YOU DIED", 60, dead_color)
    end_score = gamebox.from_text(25*w, 21*h, "Your score:  " + str(score), 50, dead_color)
    current_high_score = gamebox.from_text(25*w, 28*h, "Highscore:  " + str(high_score), 50, dead_color)
    press_h = gamebox.from_text(25*w, 35*h, "PRESS 'H' TO PLAY AGAIN", 30, dead_color)
    camera.draw(you_died)
    camera.draw(end_score)
    camera.draw(current_high_score)
    camera.draw(press_h)


################## GAME ON/OFF #######################
game_status = "start"


def check_if_killed():
    '''
    Changes game status when wackman has been killed
    :return: none
    '''
    global game_status
    for cobra in cobras:
        if abs(wackman[0].x - cobra[0].x) < w and abs(wackman[0].y - cobra[0].y) < h:
            game_status = "over"


def check_if_start(keys):
    '''
    Checks for a space to start the game
    :param keys: Space
    :return: none
    '''
    global game_status
    if pygame.K_SPACE in keys:
        game_status = "play"


def check_if_play_again(keys):
    '''
    Checks for an 'h' to return to start screen
    :param keys: h
    :return: none
    '''
    global score
    global game_status
    if pygame.K_h in keys:
        game_status = "start"
        score = 0


def check_if_won():
    global background_color
    global wall_color
    global title_color
    global bloop_list
    if score % 24800 == 0 and len(bloop_list) != 414:
        for i in range(3, 49, 2):
            x = i * w
            for j in range(3, 39, 2):
                y = j * h
                if [x, y] not in bloop_list:
                    bloop_list.append([x, y])
    if score == 24800:
        background_color = 'green'
        wall_color = 'black'
        title_color = 'green'
    if score == 49600:
        background_color = 'black'
        wall_color = 'red'
        title_color = 'black'


################### Interactives #####################

#### WACKMAN #####

step_count = 0
frame = 0
frames = 0


def make_wackman(x, y):
    '''
    makes wackman
    :param x: x-coordinate
    :param y: y-coordinate
    :return: list of images from sprite
    '''
    global frames
    images = gamebox.load_sprite_sheet("george.png", 4, 4)
    frames = len(images)
    image_list = []
    for image in images:
        image = pygame.transform.scale(image, (width//25, height//20))
        image_list.append(gamebox.from_image(x, y, image))
    return image_list


wackman = make_wackman(width//2, height//2)


def draw_wackman(image_list, keys):
    '''
    draws images in wackman, makes him run
    :param image_list: images from sprite, wackman
    :param keys: arrows to move
    :return: none
    '''
    global frame
    run_right = [image_list[7], image_list[15]]
    run_left = [image_list[5], image_list[13]]
    run_up = [image_list[6], image_list[14]]
    run_down = [image_list[4], image_list[12]]
    if pygame.K_RIGHT in keys:
        camera.draw(run_right[int(frame) % 2])
    elif pygame.K_LEFT in keys:
        camera.draw(run_left[int(frame) % 2])
    elif pygame.K_UP in keys:
        camera.draw(run_up[int(frame) % 2])
    elif pygame.K_DOWN in keys:
        camera.draw(run_down[int(frame) % 2])
    else:
        camera.draw(image_list[0])
    frame += .3


def move_wackman(keys):
    '''
    moves wackman in accordance to keys
    :param keys: arrows
    :return: none
    '''
    if pygame.K_RIGHT in keys:
        for each in wackman:
            each.x += wackman_speed * w / 25

    if pygame.K_LEFT in keys:
        for each in wackman:
            each.x -= wackman_speed * w / 25

    if pygame.K_UP in keys:
        for each in wackman:
            each.y -= wackman_speed * h / 25

    if pygame.K_DOWN in keys:
        for each in wackman:
            each.y += wackman_speed * h / 25
    for each in wackman:
        each.x %= width


def wackman_from_walls():
    '''
    makes wackman not hit walls
    :return:
    '''
    global walls
    global wackman
    for wall in walls:
        for the_frame in wackman:
            the_frame.move_to_stop_overlapping(wall)


##### COBRAS #####

def make_cobras(x, y):
    '''
    makes image list from sprite
    :param x: x-coordinate
    :param y: y-coordinate
    :return: image list
    '''
    global frames
    cobra_images = gamebox.load_sprite_sheet("king_cobra-red.png", 4, 3)
    frames = len(cobra_images)
    cobra_image_list = []
    for image in cobra_images:
        image = pygame.transform.scale(image, (width//25, height//20))
        cobra_image_list.append(gamebox.from_image(x, y, image))
    return cobra_image_list


cobra1 = make_cobras(int(3*w), int(3*h))
cobra2 = make_cobras(int(47*w), int(3*h))
cobra3 = make_cobras(int(3*w), int(37*h))
cobra4 = make_cobras(int(47*w), int(31*h))
cobra5 = make_cobras(int(23*w), int(33*h))
cobras = [cobra1, cobra2, cobra3, cobra4, cobra5]


def draw_cobras():
    '''
    draws the list of cobras in accordance to how it is moving
    :return: none
    '''
    global frame
    global cobras

    for cobra in cobras:
        run_right = [cobra[3], cobra[4], cobra[5]]
        run_left = [cobra[9], cobra[10], cobra[11]]
        run_up = [cobra[0], cobra[1], cobra[2]]
        run_down = [cobra[6], cobra[7], cobra[8]]
        if cobra[0].speedx > 0:
            camera.draw(run_right[int(frame) % 3])
        elif cobra[0].speedx < 0:
            camera.draw(run_left[int(frame) % 3])
        elif cobra[0].speedy < 0:
            camera.draw(run_up[int(frame) % 3])
        elif cobra[0].speedy > 0:
            camera.draw(run_down[int(frame) % 3])
        else:
            camera.draw(cobra[6])


cobra_speedx = cobra_speed * w / 25
cobra_speedy = cobra_speed * h / 25
timer = 0
for cobra in cobras:
    for each in cobra:
        each.speedx = cobra_speedx
        each.speedy = cobra_speedy
stopcount1 = 0
stopcount2 = 0
stopcount3 = 0
stopcount4 = 0
stopcount5 = 0

def move_cobra1():
    '''
    moves the cobras around
    :return: none
    '''
    global cobra_speedx
    global cobra_speedy
    global timer
    global stopcount1
    if cobra1[0].speedx == 0 and cobra1[0].speedy == 0:
        if stopcount1 % 4 == 0:
            for each in cobra1:
                each.speedx = -cobra_speedx
                each.speedy = cobra_speedy
        if stopcount1 % 4 == 1:
            for each in cobra1:
                each.speedx = -cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount1 % 4 == 2:
            for each in cobra1:
                each.speedx = cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount1 % 4 == 3:
            for each in cobra1:
                each.speedx = cobra_speedx
                each.speedy = cobra_speedy
        stopcount1 += 1
    for each in cobra1:
        each.x = each.x % width
        each.move_speed()
    if timer % 60 == 0:
        cobra_speedx *= -1
    if timer % 84 == 0:
        cobra_speedy *= -1
    timer += 1


def move_cobra2():
    '''
    moves the cobras around
    :return: none
    '''
    global cobra_speedx
    global cobra_speedy
    global timer
    global stopcount2
    if cobra2[0].speedx == 0 and cobra2[0].speedy == 0:
        if stopcount2 % 4 == 0:
            for each in cobra2:
                each.speedx = -cobra_speedx
                each.speedy = cobra_speedy
        if stopcount2 % 4 == 1:
            for each in cobra2:
                each.speedx = -cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount2 % 4 == 2:
            for each in cobra2:
                each.speedx = cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount2 % 4 == 3:
            for each in cobra2:
                each.speedx = cobra_speedx
                each.speedy = cobra_speedy
        stopcount2 += 1
    for each in cobra2:
        each.x = each.x % width
        each.move_speed()


def move_cobra3():
    '''
    moves the cobras around
    :return: none
    '''
    global cobra_speedx
    global cobra_speedy
    global timer
    global stopcount3
    if cobra3[0].speedx == 0 and cobra3[0].speedy == 0:
        if stopcount3 % 4 == 0:
            for each in cobra3:
                each.speedx = -cobra_speedx
                each.speedy = cobra_speedy
        if stopcount3 % 4 == 1:
            for each in cobra3:
                each.speedx = -cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount3 % 4 == 2:
            for each in cobra3:
                each.speedx = cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount3 % 4 == 3:
            for each in cobra3:
                each.speedx = cobra_speedx
                each.speedy = cobra_speedy
        stopcount3 += 1
    for each in cobra3:
        each.x = each.x % width
        each.move_speed()


def move_cobra4():
    '''
    moves the cobras around
    :return: none
    '''
    global cobra_speedx
    global cobra_speedy
    global timer
    global stopcount4
    if cobra4[0].speedx == 0 and cobra4[0].speedy == 0:
        if stopcount4 % 4 == 0:
            for each in cobra4:
                each.speedx = -cobra_speedx
                each.speedy = cobra_speedy
        if stopcount4 % 4 == 1:
            for each in cobra4:
                each.speedx = -cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount4 % 4 == 2:
            for each in cobra4:
                each.speedx = cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount4 % 4 == 3:
            for each in cobra4:
                each.speedx = cobra_speedx
                each.speedy = cobra_speedy
        stopcount4 += 1
    for each in cobra4:
        each.x = each.x % width
        each.move_speed()


def move_cobra5():
    '''
    moves the cobras around
    :return: none
    '''
    global cobra_speedx
    global cobra_speedy
    global timer
    global stopcount5
    if cobra5[0].speedx == 0 and cobra5[0].speedy == 0:
        if stopcount5 % 4 == 0:
            for each in cobra5:
                each.speedx = -cobra_speedx
                each.speedy = cobra_speedy
        if stopcount5 % 4 == 1:
            for each in cobra5:
                each.speedx = -cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount5 % 4 == 2:
            for each in cobra5:
                each.speedx = cobra_speedx
                each.speedy = -cobra_speedy
        if stopcount5 % 4 == 3:
            for each in cobra5:
                each.speedx = cobra_speedx
                each.speedy = cobra_speedy
        stopcount5 += 1
    for each in cobra5:
        each.x = each.x % width
        each.move_speed()


def cobras_from_walls():
    '''
    makes the cobra not hit walls
    :return: none
    '''
    global walls
    global cobras
    for wall in walls:
        for cobra in cobras:
            for image in cobra:
                image.move_to_stop_overlapping(wall)

##### WALLS ######


start_walls = [
    gamebox.from_color(25*w, 5*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 15*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 25*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 35*h, wall_color, width, 2*h)
]


walls = [
    gamebox.from_color(25*w, 39*h, wall_color, width, 2*h), #Bottom
    gamebox.from_color(25*w, h, wall_color, width, 2*h), #top
    gamebox.from_color(w, 10*h, wall_color, 2*w, 18*h), #left top
    gamebox.from_color(49*w, 10*h, wall_color, 2*w, 18*h), #right top
    gamebox.from_color(w, 30*h, wall_color, 2*w, 18*h), #left bottom
    gamebox.from_color(49*w, 30*h, wall_color, 2*w, 18*h), #right bottom
    gamebox.from_color(42*w, 35*h, scoreboard_color, 12*w, 6*h), #scoreboard
    gamebox.from_color(7*w, 5*h, wall_color, 6*w, 2*h), #a
    gamebox.from_color(9*w, 9*h, wall_color, 2*w, 6*h), #b
    gamebox.from_color(5*w, 10*h, wall_color, 2*w, 4*h), #c
    gamebox.from_color(6*w, 15*h, wall_color, 8*w, 2*h), #d
    gamebox.from_color(16*w, 5*h, wall_color, 8*w, 2*h), #e
    gamebox.from_color(13*w, 10*h, wall_color, 2*w, 8*h), #f
    gamebox.from_color(5*w, 23*h, wall_color, 2*w, 10*h), #g
    gamebox.from_color(9*w, 20*h, wall_color, 2*w, 4*h), #h
    gamebox.from_color(13*w, 19*h, wall_color, 2*w, 6*h), #i
    gamebox.from_color(17*w, 15*h, wall_color, 2*w, 6*h), #j
    gamebox.from_color(19*w, 13*h, wall_color, 2*w, 2*h), #k
    gamebox.from_color(18*w, 9*h, wall_color, 4*w, 2*h), #l
    gamebox.from_color(23*w, 7*h, wall_color, 2*w, 10*h), #m
    gamebox.from_color(31*w, 5*h, wall_color, 10*w, 2*h), #n
    gamebox.from_color(27*w, 10*h, wall_color, 2*w, 4*h), #o
    gamebox.from_color(33*w, 9*h, wall_color, 6*w, 2*h), #p
    gamebox.from_color(31*w, 11*h, wall_color, 2*w, 2*h), #q
    gamebox.from_color(26*w, 15*h, wall_color, 8*w, 2*h), #r
    gamebox.from_color(22*w, 17*h, wall_color, 4*w, 2*h), #s
    gamebox.from_color(21*w, 23*h, wall_color, 2*w, 10*h), #t
    gamebox.from_color(17*w, 22*h, wall_color, 2*w, 4*h), #u
    gamebox.from_color(13*w, 26*h, wall_color, 2*w, 4*h), #v
    gamebox.from_color(16*w, 27*h, wall_color, 4*w, 2*h), #w
    gamebox.from_color(9*w, 27*h, wall_color, 2*w, 6*h), #x
    gamebox.from_color(11*w, 31*h, wall_color, 6*w, 2*h), #y
    gamebox.from_color(5*w, 33*h, wall_color, 2*w, 6*h), #z
    gamebox.from_color(12*w, 35*h, wall_color, 8*w, 2*h), #A
    gamebox.from_color(19*w, 35*h, wall_color, 2*w, 6*h), #B
    gamebox.from_color(19*w, 31*h, wall_color, 6*w, 2*h), #C
    gamebox.from_color(25*w, 35*h, wall_color, 6*w, 2*h), #D
    gamebox.from_color(25*w, 32*h, wall_color, 2*w, 4*h), #E
    gamebox.from_color(25*w, 24*h, wall_color, 2*w, 8*h), #F
    gamebox.from_color(29*w, 19*h, wall_color, 6*w, 2*h), #G
    gamebox.from_color(33*w, 15*h, wall_color, 2*w, 2*h), #H
    gamebox.from_color(35*w, 15*h, wall_color, 2*w, 6*h), #I
    gamebox.from_color(39*w, 11*h, wall_color, 2*w, 14*h), #J
    gamebox.from_color(44*w, 5*h, wall_color, 4*w, 2*h), #K
    gamebox.from_color(44*w, 9*h, wall_color, 4*w, 2*h), #L
    gamebox.from_color(44*w, 13*h, wall_color, 4*w, 2*h), #M
    gamebox.from_color(44*w, 17*h, wall_color, 4*w, 2*h), #N
    gamebox.from_color(33*w, 21*h, wall_color, 2*w, 2*h), #O
    gamebox.from_color(29*w, 24*h, wall_color, 2*w, 4*h), #P
    gamebox.from_color(29*w, 30*h, wall_color, 2*w, 4*h), #Q
    gamebox.from_color(32*w, 35*h, wall_color, 4*w, 2*h), #R
    gamebox.from_color(33*w, 30*h, wall_color, 2*w, 12*h),  # S
    gamebox.from_color(37*w, 24*h, wall_color, 2*w, 8*h), #T
    gamebox.from_color(40*w, 29*h, wall_color, 8*w, 2*h), #U
    gamebox.from_color(45*w, 26*h, wall_color, 2*w, 8*h), #V
    gamebox.from_color(44*w, 21*h, wall_color, 4*w, 2*h), #W
    gamebox.from_color(41*w, 23*h, wall_color, 2*w, 6*h) #X

]

dead_walls = [
    gamebox.from_color(25*w, 15*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 21*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 28*h, wall_color, width, 2*h),
    gamebox.from_color(25*w, 35*h, wall_color, width, 2*h)
]


def draw_dead_walls():
    for wall in dead_walls:
        camera.draw(wall)


def draw_start_walls():
    for wall in start_walls:
        camera.draw(wall)


def draw_walls():
    '''
    draws all those walls
    :return: none
    '''
    for wall in walls:
        camera.draw(wall)


##### BLOOPS #####

bloop_list = []
for i in range(3, 49, 2):
    x = i*w
    for j in range(3, 39, 2):
        y = j*h
        bloop_list.append([x, y])


def draw_bloops():
    '''
    draws all those bloops
    :return: none
    '''
    global score
    global w
    global h
    for coordinate in bloop_list:
        camera.draw(gamebox.from_circle(coordinate[0], coordinate[1], bloop_color, int(w/3)))
    if game_status == "play":
        for bloop in bloop_list:
            if abs(bloop[0] - wackman[0].x) < w/2:
                if abs(bloop[1] - wackman[0].y) < h/2:
                    bloop_list.pop(bloop_list.index(bloop))
                    score += 100


def draw_interactives(keys):
    '''
    draws each interactive based on the game status
    :param keys: h, space, or arrows
    :return: none
    '''
    global wackman
    global cobra1
    global cobra2
    global cobra3
    global cobra4
    global cobra5
    global cobras
    if game_status == "start":
        wackman = make_wackman(width // 2, height // 2)
        cobra1 = make_cobras(int(3 * w), int(3 * h))
        cobra2 = make_cobras(int(47 * w), int(3 * h))
        cobra3 = make_cobras(int(3 * w), int(37 * h))
        cobra4 = make_cobras(int(47 * w), int(31 * h))
        cobra5 = make_cobras(int(23 * w), int(33 * h))
        cobras = [cobra1, cobra2, cobra3, cobra4, cobra5]
        wackman_from_walls()
        draw_bloops()
        draw_wackman(wackman, keys)
        draw_cobras()
        draw_walls()
    if game_status == "play":
        draw_bloops()
        wackman_from_walls()
        cobras_from_walls()
        draw_wackman(wackman, keys)
        draw_cobras()
        move_wackman(keys)
        move_cobra1()
        move_cobra2()
        move_cobra3()
        move_cobra4()
        move_cobra5()
        draw_walls()
    if game_status == "over":
        draw_bloops()
        draw_cobras()
        draw_walls()

################## STATS ##################
score = 0


def draw_stats():
    '''
    draws stats in stat box
    :return: none
    '''
    camera.draw(gamebox.from_text(42*w, 33*h, str(score), 50, stats_text_color, 0, 5))  # score


##################### TICK #################


def tick(keys):
    global bloop_list

    camera.clear(background_color)

    if game_status == "start":
        if len(bloop_list) != 414:
            bloop_list = []
            for i in range(3, 49, 2):
                x = i * w
                for j in range(3, 39, 2):
                    y = j * h
                    bloop_list.append([x, y])
        draw_interactives(keys)
        draw_stats()
        draw_start_walls()
        draw_title()
        draw_start_text()
        check_if_start(keys)

    if game_status == "play":
        check_if_won()
        draw_interactives(keys)
        draw_stats()
        draw_title()
        check_if_killed()

    if game_status == "over":
        draw_interactives(keys)
        draw_stats()
        draw_dead_walls()
        draw_title()
        handle_high_score()
        draw_dead_text()
        check_if_play_again(keys)
    camera.display()


gamebox.timer_loop(60, tick)



