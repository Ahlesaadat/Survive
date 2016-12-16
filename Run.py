'''
    Intro to CS
    Final Project - Survive!
    Version 3.4.1
    Seyed Mohammad Ahlesaadat
    Yousra El Hassan
'''

import pygame, random, math, time
pygame.init()

w = 700
h = 500

screen = pygame.display.set_mode((w,h))

background = pygame.image.load('bg-1.png')
background = pygame.transform.scale(background, (w, h))

splash = pygame.image.load('splash4.png')
splash = pygame.transform.scale(splash, (w, h))

space_ship_0 = pygame.image.load('Shield_0.png').convert_alpha()
space_ship_1 = pygame.image.load('Shield_1.png').convert_alpha()

earth = pygame.image.load('Earth.png')

shield_text = pygame.image.load('shield_stat.png')

pygame.display.set_caption("Survive!")

health_battery = [pygame.image.load('H1.tiff'),
                  pygame.image.load('H2.tiff'),
                  pygame.image.load('H3.tiff'),
                  pygame.image.load('H4.tiff'),
                  pygame.image.load('H5.tiff'),
                  pygame.image.load('H6.tiff'),
                  pygame.image.load('H7.tiff'),
                  pygame.image.load('H8.tiff'),
                  pygame.image.load('H9.tiff'),
                  pygame.image.load('H10.tiff')]

font = pygame.font.SysFont('monospace', 30, False, False)

font2 = pygame.font.SysFont('courier new', 70, True, False)

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red   = (255, 0, 0)
green = (0, 255, 0)


# Player's Score / High Score
score = 0

Game_on = True

# Game Intro

def splash_screen():

    intro = True
    
    while intro:
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_c:
                    pygame.QUIT()
    
        screen.fill(white)
        screen.blit(splash, (0,0))
        pygame.display.update()
        clock.tick(15)

def end_screen():
    
    intro = True
    
    while intro:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                if event.key == pygame.K_c:
                    pygame.QUIT()

        screen.fill(black)
        background = pygame.image.load('end3.png')
        background = pygame.transform.scale(background, (w, h))
        screen.blit(background, (0,0))
        screen.blit(score_graphic_f, (303,290))
        pygame.display.update()
        clock.tick(15)

Game_on = True

class Player():
    
    def __init__(self, x, y, width, height, Vx, Vy):
        
        self.health = 100
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Vx = Vx
        self.Vy = Vy
        
        space_ship_0 = pygame.image.load('shield_0.png').convert_alpha()
        self.rect = space_ship_0.get_rect()
        self.rect = pygame.Rect((x, y), (width, height))
    
        space_ship_1 = pygame.image.load('shield_1.png').convert_alpha()
        self.rect2 = space_ship_1.get_rect()
        self.rect2 = pygame.Rect((x, y), (width, height))

    def isDead(self):
    
        if self.health <= 0:
            return True
        else:
            return False
        
    # Takes the screen, x position, y position
    def display(self, shield_on = False):
            
        # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        rect = (self.x, self.y, self.width, self.height)
        rect2 = (self.x, self.y, self.width, self.height)

        if shield_on:
            screen.blit(space_ship_1, (rect[0],rect[1]))
        else:
            screen.blit(space_ship_0, (rect[0],rect[1]))

    def move(self):

        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

        self.x += self.Vx
        self.y += self.Vy

        # Keeps user in screen
        if self.x < 0:
            self.x = 0
        if (self.x + 79) > w:
            self.x = (w - 79)
        if self.y < 0:
            self.y = 0
        if (self.y + 40) > h:
            self.y = (h - 40)

class Particle():
                     
    def __init__(self, color, size, angle, player):
       
        self.x = 350
        self.y = 250
        self.thickness = 1

        self.size = size # Height / Width
        self.color = color
        self.thickness = 0
        
        self.rocket = pygame.image.load('missile3.png').convert_alpha()

        y_diff = player.y - self.y
        x_diff = player.x - self.x
        self.rect = pygame.Rect((x, y), (size, size))

        if player.x < 350:
            self.angle = 180 + math.degrees(math.atan(y_diff/(x_diff+0.000000001)))
            self.rocket = pygame.transform.rotate(self.rocket, self.angle - 180)
        else:
            self.angle = math.degrees(math.atan(y_diff/x_diff))
            self.rocket = pygame.transform.rotate(self.rocket, self.angle)

    def display(self):
        rect = (self.x, self.y, self.size, self.size)
        screen.blit(self.rocket, (rect[0],rect[1]))
    
    def move(self):

        bullet_speed = 10
        self.x += bullet_speed * math.cos( math.radians(-self.angle) )
        self.y += -bullet_speed * math.sin( math.radians(-self.angle) )
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

# Player's Size

o_width = 20
o_height = 20

# Player's Original Position

x = 10
y = 10

# Player's Original Velocity

Vx = 0
Vy = 0

user = Player(x, y, o_width, o_height, Vx, Vy)

# making multiple particles
angles = [10, 200, 300, -40]

particles = []

count = 0

current_battery_status_list_value = 0
current_battery_status = health_battery[current_battery_status_list_value]

splash_screen()

space_press = False
new_time =time.time()

total_shields = 10

shield_on = False
del_particles = True

while Game_on:
    
    hs = open('High_Scores.txt', 'r')
    high_score = int(hs.readline())
    hs.close()
    
    high_score_graphic = font.render("High Score " + str(high_score), 1, white)
    screen.blit(high_score_graphic,(0,0))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.QUIT()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                user.Vx = -5
            elif event.key == pygame.K_d:
                user.Vx = 5
            elif event.key == pygame.K_w:
                user.Vy = -5
            elif event.key == pygame.K_s:
                user.Vy = 5
            elif event.key == pygame.K_x and del_particles:
                particles = []
                del_particles = False

            elif event.key == pygame.K_SPACE and space_press == False and total_shields > 3:
                new_time = time.time()
                space_press = True
        
        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_a or event.key == pygame.K_d:
                user.Vx = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                user.Vy = 0
            elif event.key == pygame.K_SPACE:
                space_press = False
                shield_on = False

    if (count % 35 == 0):
        
        ang = random.choice(angles)
        particles.append(Particle(red, 5, ang, user))
        score += 10
        score_graphic = font.render("Score " + str(score), 1, white)
        score_graphic_f = font2.render(str(score), 1, white)

        
        total_shields += 1
        
        if total_shields > 10:
            total_shields = 10

    count += 1
    
    curr_time = time.time()
    
    if space_press:
        if (curr_time - new_time) > 0.3:
            new_time = time.time()
            total_shields -= 1
            
        shield_on = total_shields > 0

    screen.fill(white)
    screen.blit(background, (0,0))


    for particle in particles:

        if particle.y > (h):
            particle.angle =  - particle.angle
            
        if particle.y < (0):
            particle.angle = - particle.angle

        if particle.x > (w - 10):
            particle.angle = 180 - particle.angle

        if particle.x < (0):
            particle.angle = 180 - particle.angle
    
        particle.move()
        particle.display()


    # Particle - Player Collisions
    
    rec_list  = []

    for particle in particles:
        rec_list.append(particle.rect)
    particle_index = user.rect.collidelist(rec_list)

    if particle_index >= 0:
        particles.remove(particles[particle_index])
        if shield_on:
            pass
        else:
            user.health -= 10
            if current_battery_status_list_value < 9:
                current_battery_status_list_value += 1
                current_battery_status = health_battery[current_battery_status_list_value]

    if user.isDead():
        pygame.time.wait(1000)
        
        
        # Reseting All Values
        
        user.health = 100
        score = 0
        particles = []
        del_particles = True
        current_battery_status_list_value = 0
        current_battery_status = health_battery[current_battery_status_list_value]
        user.x = 10
        user.y = 10
        shield_on = False
        screen.fill(white)
        end_screen()
        splash_screen()

    if score > high_score:
        hs = open('High_Scores.txt', 'w')
        hs.write(str(score))
        hs.close()

    user.move()
    user.display(shield_on)
    screen.blit(earth,(305, 200))
    screen.blit(score_graphic, (15, 445))
    screen.blit(high_score_graphic, (15, 465))
    screen.blit(current_battery_status,(487, 380))




    if total_shields > 3 and not space_press:
        screen.blit(shield_text, (600,7))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
