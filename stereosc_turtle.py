# i thought this would be funny

import turtle, stereoscopy

turtle.speed(0)

dims = (turtle.window_width(), turtle.window_height())
ren = stereoscopy.Renderer(dims, 100)

@ren.draw
def draw_line(pos1, pos2, color):
    turtle.penup()
    turtle.goto(pos1)
    turtle.pendown()
    turtle.goto(pos2)
    turtle.penup()

@ren.draw
def anchor(x, y):
    return (x, y)

cube = stereoscopy.Mesh(
    [0,0,2],
    stereoscopy.HYPERCUBE_VERTICES,
    stereoscopy.HYPERCUBE_EDGES
    )
cube.setRotation(1,1,1)
ren.render(cube)
