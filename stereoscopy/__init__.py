import sys
import stereoscopy.matrices as matrices # numpy fallback

WHITE = (255,255,255)
DRAWPIXEL_WARNING = """draw_pixel should be defined with the .draw decorator first! i.e.:
        
ren = stereoscopy.Renderer()

@ren.draw
def draw_pixel(position, color):
    [...]
It's a good idea to make sure whatever you put in there is fast!
You can make it faster by providing shortcuts for draw_line, clear_canvas, etc."""

class Renderer:
    __FUNC_WHITELIST = (
        'draw_pixel',
        'draw_line',
        'frame_update',
        'clear_canvas',
        'anchor'
        )

    def __init__(self, dims, scale):
        self.dimensions = dims
        self.scale = scale
        self.position = Vector3(0,0,0)
        self.rotmtx = matrices.rotationMatrix(0,0,0)
        pass

    def get_width(self): return self.dimensions[0]
    def get_height(self): return self.dimensions[1]
    def setPosition(self, pos): self.position = Vector3(*pos)
    def setRotation(self, yaw, pitch, roll):
        self.rotmtx = matrices.rotationMatrix(yaw, pitch, roll)

    def draw(self, func): # Draw function override decorator
        fname = func.__name__
        if fname in self.__FUNC_WHITELIST:
            setattr(self, func.__name__, func)
        else:
            e = f"{fname} may not be overridden"
            raise PermissionError(e)

    def draw_pixel(self, position, color):
        e = DRAWPIXEL_WARNING
        raise NotImplementedError(e)

    def draw_line(self, pos1, pos2, color):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        longest = max(abs(dx), abs(dy))
        x = pos1[0]
        y = pos1[1]
        for i in range(int(longest)):
            self.draw_pixel((int(x), int(y)), color)
            x += dx / longest
            y += dy / longest

    def clear_canvas(self):
        # slow. inefficient. may leak memory depending on the canvas
        if not hasattr(self, 'clear_canvas_warned'):
            sys.stderr.write("(stereoscopy) warning: clear_canvas has not yet been defined (this is not required, but defining it will likely drastically improve performance!)\n")
            self.clear_canvas_warned = True
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                self.draw_pixel((x, y), 0)

    def frame_update(self):
        if not hasattr(self, 'frame_update_warned'):
            sys.stderr.write("(stereoscopy) warning: frame_update has not yet been defined (ignore this if the frame updates automatically!)\n")
            self.frame_update_warned = True

    # scales 2d center-anchored coords based on hyperbolic curve at z
    # returns 2d center-anchored coords. this is kind of where 3d magic happens
    # TODO: the math on this is fucky. it can be improved.
    def coord3(self, x, y, z, fov=0.5):
        if z > 0: # clip non-positive values
            c = self.scale/(z**fov)
            return True, (x*c, y*c)
        return False, (-self.get_width() - 1, -self.get_height() - 1) # tentative - just need it offscreen

    # converts center-anchored coords to top left anchored ones (by default)
    def anchor(self, x, y):
        return (int(x+self.get_width()/2), int(y+self.get_height()/2))

    def drawLine3(self, x1, y1, z1, x2, y2, z2, color=WHITE):
        c1 = self.coord3(x1, y1, z1)
        c2 = self.coord3(x2, y2, z2)
        if not(c1[0]) or not(c2[0]):
            return # just don't try to draw the line
        ac1 = self.anchor(*c1[1])
        ac2 = self.anchor(*c2[1])
        self.draw_line(ac1, ac2, color)

    def render(self, mesh):
        g = mesh.getTransformedGeometry()
        for e in mesh.getEdges():
            v1 = matrices.vecMtxMultiply3(self.rotmtx, g[e[0]] - self.position)
            v2 = matrices.vecMtxMultiply3(self.rotmtx, g[e[1]] - self.position)
            self.drawLine3(*v1, *v2)


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __getitem__(self, index): # for unpack
        vec = (self.x, self.y, self.z)
        if hasattr(index, '__getitem__'):
            return [vec[i] for i in index]
        else:
            return vec[index]

    def normalize(self):
        raise NotImplementedError

    def magnitude(self):
        raise NotImplementedError

    def __mul__(self, other):
        if type(other) == int:
            return Vector3(self.x*other, self.y*other, self.z*other)
        elif hasattr(other, '__getitem__'):
            return Vector3(self.x*other[0], self.y*other[1], self.z*other[2])
        return NotImplemented

    def __rmul__(self, other):
        if type(other) == int:
            return Vector3(self.x*other, self.y*other, self.z*other)
        return NotImplemented

    def __add__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector3(self.x+other[0], self.y+other[1], self.z+other[2])
        return NotImplemented

    def __sub__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector3(self.x-other[0], self.y-other[1], self.z-other[2])
        return NotImplemented

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)


class Mesh:
    def __init__(self, position, vertices, edges):
        self.rotmatrix = matrices.rotationMatrix(0, 0, 0)
        self.position = Vector3(*position)
        self.vertices = [Vector3(*v) for v in vertices]
        self.edges = edges

    def getTransformedGeometry(self):
        transformed = []
        for v in self.vertices:
            v_temp = Vector3(*matrices.vecMtxMultiply3(self.rotmatrix, v))
            transformed.append(v_temp + self.position)
        return tuple(transformed)

    def setRotation(self, yaw, pitch, roll):
        self.rotmatrix = matrices.rotationMatrix(yaw, pitch, roll)

    def setPosition(self, pos):
        self.position = Vector3(*pos)

    def getEdges(self): return self.edges


HYPERCUBE_VERTICES = (
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

HYPERCUBE_EDGES = (
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