import pygame
pygame.init()
song = pygame.mixer.Sound('music/s2.ogg')
clock = pygame.time.Clock()
song.play()
while True:
    clock.tick(60)
pygame.quit()
