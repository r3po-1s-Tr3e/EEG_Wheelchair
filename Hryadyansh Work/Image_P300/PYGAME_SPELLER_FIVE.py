import time
from pylsl import StreamInfo, StreamOutlet
import sys, os
import pygame, random, os, sys
import numpy as np

timeout = 32
dimension_image = 64  # Set the dimension of the image

def generate_random_array(block_length, block_count):
    randoms_array = []
    for blocks in range(block_count):
        nums = np.arange(block_length)
        np.random.shuffle(nums)
        if len(randoms_array) > 0 and nums[0] == randoms_array[-1]:
            nums[0], nums[-1] = nums[-1], nums[0]
        randoms_array.extend(nums)
    return randoms_array

def offline():
    info = StreamInfo('Markers', 'ImageMarkers', 1, 0, 'string', 'myuidw43536')
    outlet = StreamOutlet(info)

    pygame.init()
    info = pygame.display.Info()
    SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode(SIZE)
    background = pygame.Surface(screen.get_size())
    screenrect = screen.get_rect()
    backgroundrect = background.get_rect()
    background.fill((0, 0, 0))
    background = background.convert()
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()
    mainloop = True
    FPS = 2

    countdown_seconds = 5
    countdown_font = pygame.font.SysFont("None", 90)

    for i in range(countdown_seconds, 0, -1):
        screen.fill((0, 0, 0))

        countdown_text = countdown_font.render(f"Count the occurrence of letter: alphabet in {i} seconds",
                                               True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2,
                                     HEIGHT // 2 - countdown_text.get_height() // 2 - 30))

        pygame.display.flip()
        pygame.time.delay(1000)
        screen.blit(background, (0, 0))
        pygame.display.flip()

    grid = "ABCDE"
    
    r = generate_random_array(block_length=5, block_count=10)
    arr = ['0', '1', '2', '3', '4']

    columns = len(grid)
    length = screenrect.width / columns
    y = screenrect.height
    vert = 3 * y / 8
    oldhighlight = 0
    numtrials = 0

    def load_images():
        images = {}
        for char in grid:
            images[char] = {
                "normal": pygame.transform.scale(pygame.image.load(f"{char}_normal.png"), (dimension_image, dimension_image)),
                "flash": pygame.transform.scale(pygame.image.load(f"{char}_flash.png"), (dimension_image, dimension_image))
            }
        return images

    images = load_images()

    def makeStandard():
        for x in range(columns):
            image = images[grid[x]]["normal"]
            image_rect = image.get_rect(center=(length * x + length / 2, vert))
            background.blit(image, image_rect.topleft)
        screen.blit(background, (0, 0))
        pygame.display.flip()

    def makeHighlighted(numtrials, oldhighlight=0):
        highlight = int(arr[r[numtrials]])
        newhighlight = highlight

        for x in range(columns):
            if x == highlight:
                image = images[grid[x]]["flash"]
            else:
                image = images[grid[x]]["normal"]
            image_rect = image.get_rect(center=(length * x + length / 2, vert))
            background.blit(image, image_rect.topleft)

        return newhighlight

    while mainloop:
        milliseconds = clock.tick(FPS)
        seconds = milliseconds / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False

        if numtrials == 50:
            pygame.quit()
            break
        else:
            makeStandard()
            oldhighlight = makeHighlighted(numtrials, oldhighlight)

            screen.blit(background, (0, 0))
            pygame.display.flip()
            outlet.push_sample([str(oldhighlight + 1)])

            print('--------------')
            print(str(oldhighlight + 1))
            print('--------------')

            numtrials += 1


