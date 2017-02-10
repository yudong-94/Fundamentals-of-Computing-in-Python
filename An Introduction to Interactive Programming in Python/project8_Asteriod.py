# Asteroid
# http://www.codeskulptor.org/#user40_jHAtxkJixIr23ig.py

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
acc = 0
f = 0.01
rock_speed_range = 10
rock_num_max = 12
started = False
rock_group = set([])
rock_num = 0
missile_group = set([])
explosion_group = set([])
highest = 0
mode = "normal mode"

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def wrap(pos):
    if pos[0] > WIDTH:
        pos[0] -= WIDTH
    elif pos[0] < 0:
        pos[0] += WIDTH
    if pos[1] > HEIGHT:
        pos[1] -= HEIGHT
    elif pos[1] < 0:
        pos[1] += HEIGHT

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        global acc
        self.angle += self.angle_vel
        self.vel[0] = (1 - f) * self.vel[0] + acc * angle_to_vector(my_ship.angle)[0]
        self.vel[1] = (1 - f) * self.vel[1] + acc * angle_to_vector(my_ship.angle)[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        wrap(self.pos)

    def shoot(self):
        global missile_group
        missile_pos = [0, 0]
        missile_vel = [0, 0]
        for i in range(0, 2):
            missile_pos[i] = self.pos[i] + self.radius * angle_to_vector(my_ship.angle)[i]
            missile_vel[i] = self.vel[i] + 6 * angle_to_vector(my_ship.angle)[i]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated == True:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        wrap(self.pos)
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False

    def collide(self, other_object):
        dis = dist(self.pos, other_object.pos)
        if dis < self.radius + other_object.radius:
            return True
        else:
            return False

def draw(canvas):
    global time, started, rock_num, score, lives, rock_group, missile_group, my_ship, highest

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship
    my_ship.draw(canvas)

    # update ship
    my_ship.update()

    # draw and update sets of sprites
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # test collision
    if group_collide(rock_group, my_ship):
        rock_num -= 1
        lives -= 1

    break_num = group_group_collide(rock_group, missile_group)
    rock_num -= break_num
    score += break_num

    # draw scores and lives
    canvas.draw_text("lives: "+str(lives), [50 ,50], 36, "White")
    canvas.draw_text("scores: "+str(score), [600 ,50], 36, "White")

    # restart game when running out of lifes
    if lives <= 0:
        started = False
        soundtrack.pause()
        if score > highest:
            highest = score

    # draw splash screen
    if not started:
        rock_group = set([])
        rock_num = 0
        missile_group = set([])
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        canvas.draw_text("Instruction: ", [150, 500], 20, "White")
        canvas.draw_text("Right/Left: Rotate clockwise/counter clockwise", [150, 525], 20, "White")
        canvas.draw_text("Up: Thrust your ship", [150, 550], 20, "White")
        canvas.draw_text("Space: shoot a missile", [150, 575], 20, "White")
        canvas.draw_text("Highest Score: "+ str(highest), [200, 125], 36, "Red")
        canvas.draw_text(mode, [300, 400], 24, "Red")
        soundtrack.rewind()
        soundtrack.play()


# timer handler that spawns a rock
def rock_spawner():
    global rock_group, rock_num, rock_num_max
    pos = [0, 0]
    vel = [0, 0]
    pos[0] = random.randrange(WIDTH)
    pos[1] = random.randrange(HEIGHT)
    vel[0] = random.randrange(-rock_speed_range, rock_speed_range) / 5.0
    vel[1] = random.randrange(-rock_speed_range, rock_speed_range) / 5.0
    ang_vel = random.randrange(-1, 1) / 5.0
    a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
    if started and rock_num < rock_num_max:
        while dist(pos, my_ship.pos) <= my_ship.radius + a_rock.radius:
            pos[0] = random.randrange(WIDTH)
            pos[1] = random.randrange(HEIGHT)
            a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        rock_num += 1

# draw and update a set of sprites
def process_sprite_group(group, canvas):
    for item in set(group):
        item.draw(canvas)
        item.update()
        if item.update():
            group.remove(item)

# handler for group collision
def group_collide(group, other_object):
    global explosion_group
    collision = False
    for item in set(group):
        if item.collide(other_object):
            group.remove(item)
            collision = True
            explosion = Sprite(item.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    return collision

def group_group_collide(group1, group2):
    remove_num = 0
    for item in set(group1):
        if group_collide(group2, item):
            group1.remove(item)
            remove_num += 1
    return remove_num

# keyboard input handler
def keydown(key):
    global acc
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = -0.05
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0.05
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        acc = 0.1
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        missile_sound.rewind()
        missile_sound.play()

def keyup(key):
    global acc
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        acc = 0
        ship_thrust_sound.pause()
        missile_sound.pause()

def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0

# adjust difficulty level
def easy():
    global rock_speed_range, mode, started, rock_num_max
    rock_speed_range = 5
    rock_num_max = 10
    mode = "easy mode"
    started = False

def normal():
    global rock_speed_range, mode, started, rock_num_max
    rock_speed_range = 10
    rock_num_max = 12
    mode = "normal mode"
    started = False

def hard():
    global rock_speed_range, mode, started, rock_num_max
    rock_speed_range = 15
    rock_num_max = 15
    mode = "hard mode"
    started = False


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.add_button('easy', easy, 100)
frame.add_label("")
frame.add_button('normal', normal, 100)
frame.add_label("")
frame.add_button('hard', hard, 100)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
