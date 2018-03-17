from __future__ import division
from utilities import files
from psychopy import core, visual, event, monitors
from psychopy.tools.coordinatetools import cart2pol
import numpy as np
import itertools
from operator import itemgetter


def is_in_co(chosen_one, field_s, x, y):
    x_lo = grid[chosen_one][0] - field_s < x
    x_hi = grid[chosen_one][0] + field_s > x
    y_lo = grid[chosen_one][1] - field_s < y
    y_hi = grid[chosen_one][1] + field_s > y
    return (x_lo and x_hi) and (y_lo and y_hi)



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

# sizes and dimensions
fov = (15.0, 10.0)
w = fov[0]
h = fov[1]
obj_size = (2.0, 2.0)
field_s = obj_size[0]/3

grid = list(itertools.product(np.linspace(-w/2, w/2, 4), np.linspace(-h/2, h/2, 3)))
grid_size = len(grid)


# game settings
healthy_am = 2
junk_am = healthy_am * 2
misc_am = grid_size - (healthy_am + junk_am)

healthy_value = 100
junk_value = -20
misc_value = -5
score = 0



# misc
score_text = visual.TextStim(win, text='score', height=1, color='black', pos=[0, h/2+2.5])
cursor = visual.Circle(win, radius=1.5, lineColor='white', autoDraw=True)


# stimuli
healthy = files.get_files('icons/healthy', '', 'png', wp=True)[0]
junk = files.get_files('icons/junk', '', 'png', wp=True)[0]
misc = files.get_files('icons/misc', '', 'png', wp=True)[0]


# generator
healthy_images = list(np.random.choice(healthy, healthy_am))
junk_images = list(np.random.choice(junk, junk_am))
misc_images = list(np.random.choice(misc, misc_am))

all_images = healthy_images + junk_images + misc_images

image_order = range(grid_size)
np.random.shuffle(image_order)

healthy_ix = image_order[:healthy_am]
junk_ix = image_order[healthy_am:healthy_am+junk_am]

images = [visual.ImageStim(win, image=all_images[i], pos=grid[image_order[i]], size=obj_size) for i in range(grid_size)]



event.clearEvents()
while event.getKeys() == []:
    [images[i].draw() for i in range(grid_size)]
    
    x, y = mouse.getPos()
    cursor.pos = [x,y]

    healthy_check = np.sum([is_in_co(i, field_s, x, y) for i in healthy_ix])
    junk_check = np.sum([is_in_co(i, field_s, x, y) for i in junk_ix])
    
    if healthy_check >= 1:
        score += healthy_value
        cursor.lineColor = 'green'
    
    elif junk_check >= 1:
        score += junk_value
        cursor.lineColor = 'red'
    
    else:
        cursor.lineColor = 'white'
        score += misc_value
    
    score_text.text = 'Your current power: {0}'.format(str(score))
    score_text.draw()
    win.flip()
win.close()
