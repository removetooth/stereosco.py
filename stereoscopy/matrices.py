import math
# Matrix math
# Taken and simplified from last year's linear algebra final

# Eventually should be changed to be object-oriented & work with magic methods
# Alternatively use this as a wrapper for numpy because what the fuck
# (This code is still good to have as a fallback because numpy isn't standard library)

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
def rotationMatrix(yaw, pitch, roll):
    sA = math.sin(yaw)
    cA = math.cos(yaw)
    yawMatrix = (
        cA,    -sA,    0,
        sA,    cA,     0,
        0,     0,      1
        )
    sB = math.sin(pitch)
    cB = math.cos(pitch)
    pitchMatrix = (
        cB,    0,      sB,
        0,     1,      0,
        -sB,   0,      cB
        )
    sG = math.sin(roll)
    cG = math.cos(roll)
    rollMatrix = (
        1,     0,      0,
        0,     cG,   -sG,
        0,     sG,    cG
        )
    temp = matrixMultiply3(yawMatrix, pitchMatrix)
    A = matrixMultiply3(temp, rollMatrix)
    return A