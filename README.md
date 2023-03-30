# stereosco.py
an experimental, canvas-agnostic 3d graphics library written in pure python. impractical, but reinventing the wheel is fun!

name is subject to change, because as it turns out, `pip install stereoscopy` already gives you some other package that already exists. damn.

i wrote all of this because- first and foremost- i want to learn 3d rendering techniques, and i think i've learned enough from my classes to be able to do it. also opengl hurts my brain, confuses my build tools, and is completely and utterly incapable of running alongside the graphics tools provided by whatever implements it. rhythm_test had this problem, where i was so deep into pygame draw calls that i ended up just converting the screen surface to an opengl texture every frame and throwing it in front of the camera. gross.

all of this, currently, works within the standard library. i want to try to make optimizations where possible - all matrix math is done manually right now, but can be sped up with the use of numpy. given that's not standard library, though, i can still use my implementation as a fallback!

i think the biggest (and only) draw of this library, as it stands, is that it works with *basically any canvas.* at the bare minimum, all you have to do is instantiate a Renderer object and tell it how to draw a pixel, like so (using pygame as an example):

```py
import pygame, stereoscopy

DIMS = (640, 480)
screen = pygame.display.set_mode(DIMS)
ren = stereoscopy.Renderer(DIMS, 150)

@ren.draw
def draw_pixel(pos, color):
    screen.set_at(pos, color)

...
```

i've even thrown in an example with turtle because i thought it would be funny.

of course, python is slow. drawing geometry pixel by pixel is slow. so, if you want, you can throw the renderer some shortcuts- drawing lines, clearing the screen, etc. if it's faster, you can override them in the same way! i'm a bit short on time to be writing documentation right now, though, so you get to figure it out yourself for the time being. sorry!

the whole thing is experimental, so everything is subject to drastic change over time, but i'm pretty happy with what i have so far.