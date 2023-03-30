# Comprehensive 3d graphics function reference
# opengl is STUPID so i'm doing it MYSELF!
import tkinter, time

DIMS = [640, 480]
PI = 3.141592653589793238 # all the digits of pi i can remember
BLACK = "black"
WHITE = "white"
# default number of iterations for Taylor expansion
# lowering this will be faster, but lower accuracy!
SINE_RES_DEFAULT = 10  # ~10 recommended

#pygame.init()
#screen = pygame.display.set_mode(DIMS)
root = tkinter.Tk()
root.title("custom 3d renderer woah")
canvas = tkinter.Canvas(root, bg=BLACK, width=DIMS[0], height=DIMS[1])
canvas.pack()



# 2d graphics library functions
# all of these functions can be modified to fit different display methods

def drawLine(x1, y1, x2, y2, col=WHITE):
    #pygame.draw.line(screen, col, [x1, y1], [x2, y2])
    canvas.create_line(x1, y1, x2, y2, fill=col)

def clearCanvas():
    #screen.fill(0)
    canvas.delete('all')

def frameUpdate():
    #pygame.display.flip()
    pass



# 3d graphics functions!

# converts center-anchored coords to top left anchored ones
def center2TopL(x, y, dimensions):
    return (int(x+dimensions[0]/2), int(y+dimensions[1]/2))

# scales center-anchored coords based on hyperbolic curve at z
# returns 2d center-anchored coords
# trying default hyp of 100
def coord3(x, y, z, hyp = 100, fov=0.5):
    if z > 0: # clip non-positive values
        c = hyp/(z**fov)
        return (x*c, y*c)
    return 0, 0

def drawLine3(x1, y1, z1, x2, y2, z2, dims=DIMS, col=WHITE):
    c1x, c1y = center2TopL(*coord3(x1, y1, z1), dims) # un-hardcode this
    c2x, c2y = center2TopL(*coord3(x2, y2, z2), dims)
    drawLine(c1x, c1y, c2x, c2y, col)



# trigonometry functions, in case they're not provided

# Approximate sine with taylor series expansion
# yeah i googled this sue me
# I don't comprehend this, but if it works, I can reference it later
def sin(x, resolution=SINE_RES_DEFAULT):
    x = x % (PI * 2) # floating point fuckup bandaid
    result = 0
    term = x
    for i in range(resolution):
        result += term
        term = -term * x * x / ((2 * i + 2) * (2 * i + 3))
    return result

# Cosine as an implementation of sine
def cos(x, resolution=SINE_RES_DEFAULT):
    return sin(x+PI/2, resolution)



# Matrix math
# Taken and simplified from last year's linear algebra final

# hardcoded 3x3 matrix multiplication
def matrixMultiply3(A, B):
    temp = []
    for i in range(9):
        temp.append(
            A[i//3*3] * B[i%3] +
            A[i//3*3+1] * B[i%3+3] +
            A[i//3*3+2] * B[i%3+6]
            )
    return tuple(temp)

# hardcoded vector-matrix3 multiplication
def vecMtxMultiply3(A, x):
    temp = []
    for i in range(0,9,3):
        temp.append(
            x[0] * A[i] +
            x[1] * A[i+1] +
            x[2] * A[i+2]
            )
    return tuple(temp)

# returns a rotation matrix- transform vertex with vecMtxMultiply3
def rotateAxes(yaw, pitch, roll):
    sA = sin(yaw)
    cA = cos(yaw)
    yawMatrix = (
        cA,    -sA,    0,
        sA,    cA,     0,
        0,     0,      1
        )
    sB = sin(pitch)
    cB = cos(pitch)
    pitchMatrix = (
        cB,    0,      sB,
        0,     1,      0,
        -sB,   0,      cB
        )
    sG = sin(roll)
    cG = cos(roll)
    rollMatrix = (
        1,     0,      0,
        0,     cG,   -sG,
        0,     sG,    cG
        )
    temp = matrixMultiply3(yawMatrix, pitchMatrix)
    A = matrixMultiply3(temp, rollMatrix)
    return A



# Cube mesh info
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
    (0.5, -0.5, -0.5), # i wanted to make a hypercube
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, 0.5, 0.5)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7), # vvv more edges for the hypercube vvv
    (8, 9), (8, 11), (8, 12), (10, 9), (10, 11), (10, 15), (14, 11), (14, 12), (14, 15), (13, 9), (13, 12), (13, 15),
    (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15)
    )

t_i = time.time()
def Update():#while 1:
    #pygame.event.get()
    clearCanvas()
    for edge in edges:
        t = time.time() - t_i
        rc = t*0.5
        rMatrix = rotateAxes(rc, rc, rc)
        v1 = vecMtxMultiply3(rMatrix, vertices[edge[0]])
        v2 = vecMtxMultiply3(rMatrix, vertices[edge[1]])
        v1_t = [v1[0], v1[1], v1[2]+2]
        v2_t = [v2[0], v2[1], v2[2]+2]
        drawLine3(*v1_t, *v2_t)
    frameUpdate()
    #time.sleep(0.016)
    root.after(16, Update) # tkinter does loops a bit differently!

Update()
root.mainloop()
