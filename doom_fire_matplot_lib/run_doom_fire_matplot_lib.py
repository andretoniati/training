import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation

fireWidth  = 30
fireHeight = 40

sizePixel  = 1

fig       = plt.figure(figsize=(1,4))
ax        = plt.axes(xlim=(0, fireWidth), ylim=(0, fireHeight))

x_grid = np.linspace(0, fireWidth * sizePixel, sizePixel)
y_grid = np.linspace(0, fireHeight * sizePixel, sizePixel)
X, Y     = np.meshgrid(x_grid, y_grid)
plt.set_cmap('bone')

global drawFire

def start():
    createDataFireStructureAndFireSource()
    anim = animation.FuncAnimation(fig, calculateFirePropagation, frames=3000, interval=1, repeat=False)
    plt.show()

def createDataFireStructureAndFireSource():
    global firePixels
    firePixels = np.zeros((fireHeight, fireWidth))
    firePixels[-1, :] = 36

def calculateFirePropagation(i):
    for column in range(0, fireWidth):
        for row in range(0, fireHeight-1):
            updateFireIntensity(row,column)
    renderFire()


def updateFireIntensity(currentRow, currentColumn):
    if currentRow >= fireHeight:
        return
    decay = int(random.random()*3)
    randomColumn = int(random.randint(0,3))
    belowPixelFireIntensity = firePixels[currentRow + 1, currentColumn]
    if belowPixelFireIntensity - decay >= 0:
        newFireIntensity = belowPixelFireIntensity - decay
    else:
        newFireIntensity = 0

    #firePixels[randomRow, randomColumn] = newFireIntensity
    if currentRow - randomColumn >= 0:
        if currentColumn + randomColumn > fireWidth:
            firePixels[currentRow, currentColumn - randomColumn] = newFireIntensity
        else:
            firePixels[currentRow, currentColumn + randomColumn - 1] = newFireIntensity
    else:
        firePixels[currentRow, currentColumn] = newFireIntensity

def renderFire():
    fig.clf()
    plt.xticks([])
    plt.yticks([])
    render_pixel = np.flip(firePixels, 0)
    drawFire = plt.pcolor(render_pixel)
    return drawFire

start()