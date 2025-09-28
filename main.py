import pygame 
import random 
import sys

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock() 
running = True

GROUND_LEVEL = 300
GRAVITY = 0.5 
JUMP_VELOCITY = -8

# bird
vertical_velocity = 0 
is_jumping = False
player_y = GROUND_LEVEL
bird_x, bird_y, = 100, 200
pipe_speed = 3

# pipes 
pipe_width = 60 
pipe_gap = 150 
pipe_x = WIDTH 
pipe_height = random.randint(100, 400)

while running: 
    # bird  
    bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)

    # pipe rectangles 
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height) 
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE: 
                vertical_velocity = JUMP_VELOCITY

    # bird physics
    vertical_velocity += GRAVITY 
    bird_y += vertical_velocity

    # bird collision
    if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe): 
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # top collision
    if bird_y <= 30: 
        bird_y = 30
        vertical_velocity = 0 

    # ground collision
    if bird_y >= 570: 
        bird_y = 570
        vertical_velocity = 0  

    # pipe movement 
    pipe_x -= pipe_speed 
    if pipe_x < -pipe_width: 
        pipe_x = WIDTH 
        pipe_height = random.randint(100, 400)    

    # draw 
    screen.fill((135, 206, 235)) # sky
    pygame.draw.rect(screen, (255, 255, 0), (bird_x, bird_y, 30, 30))  # bird

    # top pipe 
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, 0, pipe_width, pipe_height))
    # bottom pipe 
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)) 

    pygame.display.flip() 
    clock.tick(60)

pygame.quit()
