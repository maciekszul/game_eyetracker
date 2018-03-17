from __future__ import division
from utilities import visang
from psychopy import core, visual, event, monitors
from psychopy.tools.coordinatetools import cart2pol
import numpy as np
import itertools
from operator import itemgetter


width, dist, res = 28, 56, (1366, 768)

# width, dist, res = 53, 64, (1920, 1080)

mon = monitors.Monitor('default')
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)


win = visual.Window(size=res,
                    color='gray',
                    fullscr=False,
                    allowGUI=False,
                    winType='pyglet',
                    units='deg',
                    monitor=mon)

mouse = event.Mouse(visible=False, win=win)


fov = (26.0, 14.0)
# fov = (42.0, 20.0)

w = fov[0]
h = fov[1]
grating_size = (2.0, 2.0)
field_s = grating_size[0]/3

grid = list(itertools.product(np.linspace(-w/2, w/2, 21), np.linspace(-h/2, h/2, 10)))
grid_size = len(grid)

circles = [visual.GratingStim(win, tex='sin', mask='gauss', size=grating_size, sf=3, autoDraw=True) for i in range(grid_size)]
center = visual.Circle(win, radius=0.5, lineColor='white', autoDraw=True)

stopwatch = core.Clock()
ITI = core.StaticPeriod(win=win)
counter = 0

event.clearEvents()
stopwatch.reset()
[circles[i].setPos(grid[i]) for i in range(grid_size)]

choice = list(np.random.randint(0,grid_size, 8))
chosen_one = np.random.choice(choice)


def set_stim(choice, chosen_one):
    [circles[i].setColor('black') for i in range(grid_size)]
    [circles[i].setColor('blue') for i in choice]
    mouse.setPos((0.0, 0.0))

def is_in_co(chosen_one, field_s, x, y):
    x_lo = grid[chosen_one][0] - field_s < x
    x_hi = grid[chosen_one][0] + field_s > x
    y_lo = grid[chosen_one][1] - field_s < y
    y_hi = grid[chosen_one][1] + field_s > y
    return (x_lo and x_hi) and (y_lo and y_hi)


def ITI_blank(t):
    ITI.start(t)
    [circles[i].setOpacity(0.0) for i in range(grid_size)]
    center.setOpacity(0.0)
    win.flip()
    [circles[i].setOpacity(1.0) for i in range(grid_size)]
    center.setOpacity(1.0)
    complete = ITI.complete()
    flip_time = win.flip()
    return complete, flip_time


set_stim(choice, chosen_one)
while event.getKeys() == []:
    for c in circles:
        c.phase += 0.05
        c.ori = np.random.uniform(-5, 5, size=1)[0]

    x, y = mouse.getPos()
    center.pos = [x,y]

    circles[chosen_one].phase += 0.1

    if is_in_co(chosen_one, field_s, x, y):
        center.lineColor = 'green'
        if stopwatch.getTime() > 0.5:
            fix_accept = core.getTime()
            choice = list(np.random.randint(0,grid_size, 8))
            chosen_one = np.random.choice(choice)
            set_stim(choice, chosen_one)
            counter += 1

            if counter == 5:
                complete, flip_time = ITI_blank(1)
                counter = 0
                print flip_time - fix_accept
            
    else:
        center.lineColor = 'white'
        stopwatch.reset()


    win.flip()
win.close()
