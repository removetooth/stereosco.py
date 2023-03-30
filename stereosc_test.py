import stereoscopy, pygame, time

DIMS = [640, 480]

pygame.init()
screen = pygame.display.set_mode(DIMS)
ren = stereoscopy.Renderer(DIMS, 150)

@ren.draw
def draw_line(pos1, pos2, color):
    pygame.draw.line(screen, color, pos1, pos2)

@ren.draw
def clear_canvas():
    screen.fill(0)

@ren.draw
def frame_update():
    pygame.display.flip()

# TODO: how about a Scene class to handle this?
cube = stereoscopy.Mesh(
    [0,0,4.5],
    stereoscopy.HYPERCUBE_VERTICES,
    stereoscopy.HYPERCUBE_EDGES
    )
cube2 = stereoscopy.Mesh(
    [2,0,4.5],
    stereoscopy.HYPERCUBE_VERTICES,
    stereoscopy.HYPERCUBE_EDGES
    )
cube3 = stereoscopy.Mesh(
    [-2,0,4.5],
    stereoscopy.HYPERCUBE_VERTICES,
    stereoscopy.HYPERCUBE_EDGES
    )

t_i = time.time()
sin = stereoscopy.matrices.math.sin
while 1:
    pygame.event.get()
    t = time.time() - t_i
    ren.clear_canvas()
    cube.setRotation(t/2, t/2, t/2)
    cube2.setPosition((2,sin(t*2),4.5))
    cube3.setPosition((-2,-sin(t*2),4.5))
    ren.setRotation(0,sin(t)/2,0)
    ren.render(cube)
    ren.render(cube2)
    ren.render(cube3)
    ren.frame_update()
    time.sleep(0.016)
