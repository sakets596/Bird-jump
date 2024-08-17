import pygame
from sys import exit
from random import randint
# from game_over import gameOver

pygame.init()

screen = pygame.display.set_mode((800, 800))
game_active = True
start_time = 0
score = 0
test_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

bird = pygame.image.load('static/images/unitytut-birdbody.png').convert_alpha()
bird = pygame.transform.scale(bird, (90, 100))  # resize the image size
bird_rect = bird.get_rect(midbottom=(100, 100))
# print(bird_rect.bottom) # value is 100 (as of y axis of the mid bottom rect)
# print(bird_rect.centerx) 
# print(bird_rect.y)

cloud = pygame.image.load('static/images/unitytut-cloud.png').convert_alpha()
cloud = pygame.transform.scale(cloud, (100,50))

# ground = pygame.Surface((800, 600))
# ground.fill('green')

buildings = pygame.image.load('static/images/flats.png').convert_alpha()
buildings = pygame.transform.scale(buildings, (600,500))

trees = pygame.image.load('static/images/Trees-procreate.png').convert_alpha()
trees = pygame.transform.scale(trees, (900, 400))

pipe = pygame.image.load('static/images/unitytut-pipe.png').convert()
pipe = pygame.transform.scale(pipe, (70, 1000))
pipe_inverted = pygame.transform.rotate(pipe, 180)
# pipe_rect = pipe.get_rect(midtop=(400, 0)) 
# print(pipe_rect.bottom) #output is 300 i.e pipe's y axis
# print(pipe_rect.y) # 0

obstacle_rect_list = []

# sound
game_over_sound = pygame.mixer.Sound('static/sound/death.mp3')
game_over_sound.set_volume(1) # value is between 0 and 1. 0 is lowest sound and 1 is full sound.
gameplay = pygame.mixer.Sound('static/sound/gameplay.mp3')
gameplay.set_volume(1)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10

            #screen.blit(snail_surface, obstacle_rect)
            # print(obstacle_rect.bottom)

            if obstacle_rect.bottom < 500:
                screen.blit(pipe, obstacle_rect)
                # print(obstacle_rect.bottom)
            else:
                screen.blit(pipe_inverted, obstacle_rect)
                # print(obstacle_rect.x)
                # pass
                # print(obstacle_rect.bottom)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # we are copying only those obstacle in obstacle list which are on the screen. Once the obstacle leaves the screen i.e -100. we are not copying it.
        # this is required because if we don't do this our list will keep on growing and slow our game.
        return obstacle_list 
    else:
        return []


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time # pygame.time.get_ticks() gives the time in millisecond since the game started. int(pygame.time.get_ticks()/1000) convers millisec in seconds
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center=(100,50))
    pygame.draw.rect(screen, '#a5d4b2', score_rect)
    # pygame.draw.rect(screen, '#a5d4b2', score_rect, 6)
    screen.blit(score_surf, score_rect)
    return current_time


# game over
bird_img = pygame.image.load('static/images/unitytut-birdbody.png')
bird_img = pygame.transform.scale(bird_img, (150,150))
bird_up_rect = bird_img.get_rect(midbottom=(400, 370))
game_over_font = pygame.font.Font(None, 50)


def gameOver():

    game_over = game_over_font.render(f"GAME OVER", False, (64,64,64))
    game_over_rect = game_over.get_rect(center=(420,400))
    pygame.draw.rect(screen, '#f22718', game_over_rect)
    # pygame.draw.rect(screen, '#a5d4b2', score_rect, 6)

    restart_game = game_over_font.render(f"Press Any Key To Start The Game Again", False, (64,64,64))
    restart_game_rect = restart_game.get_rect(center=(420,550))

    last_game_score = game_over_font.render(f"You Score: {score}", False, (64,64,64))
    last_game_score_rect = last_game_score.get_rect(center=(420,450))
    pygame.draw.rect(screen, '#a5d4b2', last_game_score_rect)

    screen.blit(game_over, game_over_rect)
    screen.blit(last_game_score, last_game_score_rect)
    screen.blit(restart_game, restart_game_rect)


obstacle_timer = pygame.USEREVENT + 1 #creating userevent. adding +1 because there are uservent which is reserved for the the pygame. You can read doc for the detail.
pygame.time.set_timer(obstacle_timer, 800) # setting the event interval 1500 is in millisec.

gravity = 1
pipe_speed = 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_jump = -1 * (gravity + 100)
                bird_rect.y = bird_rect.y + bird_jump
                gravity = 1  # resetting gravity to 1 after jump
            
            if event.type == obstacle_timer:
                if randint(0,1): # it will return 0 or 1. 0 means false 1 means true. This is to either spawn snail or fly.
                    obstacle_rect_list.append(pipe.get_rect(midtop=(800, randint(-800, -600)))) # we want snail position to be random from 900 to 1100 px
                else:
                    obstacle_rect_list.append(pipe_inverted.get_rect(midtop=(800, randint(300, 600))))
                    # pass
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bird_rect = bird.get_rect(midbottom=(100, 100))
                gravity = 1
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        gameplay.play()
        if bird_rect.y > 900:
            game_active = False
            gameplay.stop()
            game_over_sound.play()

        screen.fill((142, 222, 230))  # clear screen after every frame execution

        screen.blit(cloud, (0,0))
        screen.blit(cloud, (100,100))
        screen.blit(cloud, (200,0))
        screen.blit(cloud, (300,100))
        screen.blit(cloud, (400,0))
        screen.blit(cloud, (500,100))
        screen.blit(cloud, (600,0))
        screen.blit(cloud, (700,100))
        screen.blit(cloud, (800,0))

        screen.blit(buildings, (100,250))
        screen.blit(trees, (-50,420))

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        for i in range(len(obstacle_rect_list)):
            if bird_rect.colliderect(obstacle_rect_list[i]):
                gameplay.stop()
                game_over_sound.play()
                game_active = False
        
        score = display_score()
        # pygame.draw.rect(screen, 'green', bird_rect)

        gravity = gravity + 0.2
        # gravity = 0
        bird_rect.y = bird_rect.y + gravity
        screen.blit(bird, bird_rect)
    else:
        # game over section
        obstacle_rect_list.clear()
        # gameOver()
        screen.fill((142, 222, 230)) 
        if bird_up_rect.y <= 220:
            bird_up_rect.y = bird_up_rect.y + 2
        else:
            bird_up_rect.y = 100
        screen.blit(bird_img, bird_up_rect)
        gameOver()

    pygame.display.update()
    clock.tick(60)