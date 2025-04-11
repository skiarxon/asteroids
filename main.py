import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
import os

def main():
    pygame.init()
    pygame.font.init()
    print ("Starting Asteroids!")
    print (f"Screen width: {SCREEN_WIDTH}")
    print (f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    score_increment = 10
    bg_image = pygame.image.load('bg.jpg')

    updatable = pygame.sprite.Group() # group for things that will be updated on screen
    drawable = pygame.sprite.Group() # group for things that are going to be drawn on screen
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # added groups as containers to player
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids,updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # moved this here or else the groups won't work properly

    while True:
        font = pygame.font.Font(None, 36)
        screen.fill("black")
        screen.blit(bg_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)

        for asteroid in asteroids:
            if  player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        for asteroid in asteroids:
            if not asteroid.alive():
               continue

            for shot in shots:
                if not shot.alive():
                   continue

                if asteroid.collides_with(shot):
                   shot.kill()
                   asteroid.split()
                   score += score_increment 
                   break  # Stop checking other shots for this asteroid     

        #screen.fill("black")

        score_text = font.render(f'Score: {score}', True, ("white"))
        screen.blit(score_text, (10, 10))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000 ##60 fps 


if __name__ == "__main__":
    main()
