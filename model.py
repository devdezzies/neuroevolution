import pygame

class Bird: 
    def __init__(self, genome, x=200, y=300): 
        self.genome = genome 
        self.x = x 
        self.y = y 
        self.velocity = 0 
        self.dead = False 
        self.radius = 20 
    
    def flap(self, jump_velocity=-8): 
        self.velocity = jump_velocity 
    
    def update(self, gravity=0.5): 
        self.velocity += gravity 
        self.y += self.velocity 

        # hit ground -> dead
        if self.y >= 600 - self.radius: 
            self.y = 600 - self.radius 
            self.dead = True

        # hit ceiling -> dead
        if self.y <= self.radius:
            self.y = self.radius
            self.dead = True

    def draw(self, screen): 
        pygame.draw.circle(screen, "yellow", (int(self.x), int(self.y)), self.radius)