import pygame 
import random 
from utils import decide_flap, next_generation
from model import Bird

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock() 
running = True
font = pygame.font.SysFont(None, 24)  # add a tiny HUD

GROUND_LEVEL = 300
GRAVITY = 0.5 
JUMP_VELOCITY = -8
POP_SIZE = 30

# pipes 
pipe_width = 60 
pipe_gap = 150 
pipe_x = WIDTH 
pipe_height = random.randint(100, 400)
pipe_speed = 5

# population
population = [[random.uniform(-1, 1) for _ in range(21)] for _ in range(POP_SIZE)]

def check_collision(bird, pipes):
    bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius*2, bird.radius*2)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False


for gen in range(100): 
    running = True
    pipe_x = WIDTH
    pipe_height = random.randint(100, 400)

    birds = [Bird(genome) for genome in population] 
    fitnesses = [0] * POP_SIZE

    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit

        screen.fill((135, 206, 235))  # sky blue

        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        # fix bottom pipe height
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - (pipe_height + pipe_gap))
        pipes = (top_pipe, bottom_pipe)

        # pipe movement 
        pipe_x -= pipe_speed 
        if pipe_x < -pipe_width: 
            pipe_x = WIDTH 
            pipe_height = random.randint(100, 400)

        # draw pipes 
        pygame.draw.rect(screen, (0, 200, 0), top_pipe)
        pygame.draw.rect(screen, (0, 200, 0), bottom_pipe)

        # HUD
        gen_surf = font.render(f"Gen: {gen+1}", True, (0,0,0))
        screen.blit(gen_surf, (10, 10))

        all_dead = True
        for i, bird in enumerate(birds):
            if not bird.dead:
                all_dead = False
                bird.update(GRAVITY)
                gap_y = pipe_height + pipe_gap / 2
                if decide_flap(bird.genome, bird.y, gap_y):
                    bird.flap()
                if check_collision(bird, pipes):
                    bird.dead = True
                else:
                    fitnesses[i] += 1  
                bird.draw(screen)

        if all_dead: 
            running = False

        pygame.display.flip()
        clock.tick(60)

    population = next_generation(population, fitnesses)
    print(f"Next gen spawned: {len(population)} genomes")

pygame.quit()
