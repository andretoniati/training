import numpy as np
import random
import pygame

sizePixel = 4

fireWidth = 100
fireHeight = 100

debug = False

fireColorsPalette = [
          (7,  7,  7), (31,  7,  7), (47, 15,  7), (71, 15,  7), (87, 23,  7), (103, 31,  7), (119, 31,  7), (143, 39,  7),
          (159, 47,  7), (175, 63,  7), (191, 71,  7), (199, 71,  7), (223, 79,  7), (223, 87,  7), (223, 87,  7), (215, 95,  7),
          (215, 95,  7), (215,103, 15), (207,111, 15), (207,119, 15), (207,127, 15), (207,135, 23), (199,135, 23), (199,143, 23),
          (199,151, 31), (191,159, 31), (191,159, 31), (191,167, 39), (191,167, 39), (191,175, 47), (183,175, 47), (183,183, 47),
          (183,183, 55), (207,207,111), (223,223,159), (239,239,199), (255,255,255)]

pygame.init()
pygame.display.set_caption("Doom Fire")

clock = pygame.time.Clock()
fonts = (pygame.font.SysFont("Arial", 10), pygame.font.SysFont("Arial", 14))

def start():
    createDataFireStructureAndFireSource()
    renderFire()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Number of frames per secong e.g. 60
        clock.tick(60)
        pygame.display.update()
        calculateFirePropagation()

def createDataFireStructureAndFireSource():
    global firePixels
    firePixels = np.zeros((fireHeight, fireWidth))
    firePixels[-1, :] = 36

def calculateFirePropagation():
    for column in range(0, fireWidth):
        for row in range(0, fireHeight-1):
            updateFireIntensity(row,column)
    renderFire()

def updateFireIntensity(currentRow, currentColumn):
    if currentRow >= fireHeight:
        return
    decay = int(random.random()*3)
    randomColumn = int(random.randint(0, 3))
    belowPixelFireIntensity = firePixels[currentRow + 1, currentColumn]
    if belowPixelFireIntensity - decay >= 0:
        newFireIntensity = belowPixelFireIntensity - decay
    else:
        newFireIntensity = 0

    if currentRow - randomColumn >= 0:
        if currentColumn + randomColumn > fireWidth:
            firePixels[currentRow, currentColumn - randomColumn] = newFireIntensity
        else:
            firePixels[currentRow, currentColumn + randomColumn - 1] = newFireIntensity
    else:
        firePixels[currentRow, currentColumn] = newFireIntensity
def renderFire():
    if debug:
        debugSize = 40
        screen = pygame.display.set_mode(
            (fireWidth * debugSize + fireWidth + 1, fireHeight * debugSize + fireHeight + 1), 0, 32)
        screen.fill((0, 0, 0))
        for row in range(0, fireHeight):
            for column in range(0, fireWidth):
                fireIntensity = int(firePixels[row, column])

                positionPixelIndex = (debugSize * column + column + 1, debugSize * row + row + 1)
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(positionPixelIndex, (debugSize, debugSize)))
                textPixelIndex = fonts[0].render(str(row) + "," + str(column), True, (120, 120, 120))
                screen.blit(textPixelIndex, (positionPixelIndex[0] + debugSize - (textPixelIndex.get_width()),
                                             positionPixelIndex[1] + textPixelIndex.get_height() / 8))
                textFireIntensity = fonts[1].render(str(fireIntensity), True, fireColorsPalette[fireIntensity])
                screen.blit(textFireIntensity, (
                positionPixelIndex[0] + debugSize / 2 - textFireIntensity.get_width() / 2,
                positionPixelIndex[1] + debugSize / 2 - textFireIntensity.get_height() / 4))

    else:
        sizeScreen = (fireWidth * sizePixel, fireHeight * sizePixel)
        screen = pygame.display.set_mode(sizeScreen,0,32)
        screen.fill(fireColorsPalette[0])
        screen.lock()

        for row in range(0, fireHeight):
            for column in range(0, fireWidth):
                fireIntensity = int(firePixels[row, column])
                pygame.draw.rect(screen, fireColorsPalette[fireIntensity], [column * sizePixel, row * sizePixel, sizePixel, sizePixel])
        screen.unlock()

start()