from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy

zPos = -60.0
yRot = 0.0

TEXTURE_COLUNA = 0
TEXTURE_CAPA_TRASEIRA = 1
TEXTURE_CAPA = 2
TEXTURE_COUNT = 3
textures = []
szTextureFiles = ["meio.bmp", "contra.bmp", "capa.bmp"]

def ProcessMenu(value):
    for iLoop in range(TEXTURE_COUNT):
        glBindTexture(GL_TEXTURE_2D, textures[iLoop])

        if value == 0:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        elif value == 1:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        elif value == 2:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
        elif value == 3:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        elif value == 4:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    glutPostRedisplay()

def SetupRC():
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    glGenTextures(TEXTURE_COUNT, textures)
    for iLoop in range(TEXTURE_COUNT):
        glBindTexture(GL_TEXTURE_2D, textures[iLoop])

        texture_image = Image.open(szTextureFiles[iLoop])
        texture_data = numpy.array(list(texture_image.getdata()), numpy.uint8)

        width, height = texture_image.size

        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, width, height, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

def ShutdownRC():
    glDeleteTextures(textures)

def SpecialKeys(key, x, y):
    global zPos, yRot

    if key == b'w':
        zPos += 1.0
    elif key == b's':
        zPos -= 1.0
    elif key == b'q':
        yRot += 1.0
    elif key == b'e':
        yRot -= 1.0

    glutPostRedisplay()

def ChangeSize(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    fAspect = float(w) / float(h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(90.0, fAspect, 1, 120)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def capa(z):
    glPushMatrix()

    glTranslatef(0.0, 0.0, -60)
    glRotatef(90, 0, 1, 0)
    glRotatef(180, 1, 0, 0)

    glBindTexture(GL_TEXTURE_2D, textures[TEXTURE_CAPA_TRASEIRA])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-10.0, -10.0, z)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(-10.0, -10.0, z - 10.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(-10.0, 10.0, z - 10.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-10.0, 10.0, z)
    glEnd()

    glPopMatrix()

def RenderScene():
    glClear(GL_COLOR_BUFFER_BIT)

    glRotatef(yRot, 0.0, 1, 0.0)
    z = zPos

    capa(z)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Tunnel")
    glutReshapeFunc(ChangeSize)
    glutKeyboardFunc(SpecialKeys)
    glutDisplayFunc(RenderScene)

    glutCreateMenu(ProcessMenu)
    glutAddMenuEntry(b"GL_NEAREST", 0)
    glutAddMenuEntry(b"GL_LINEAR", 1)
    glutAddMenuEntry(b"GL_NEAREST_MIPMAP_NEAREST", 2)
    glutAddMenuEntry(b"GL_NEAREST_MIPMAP_LINEAR", 3)
    glutAddMenuEntry(b"GL_LINEAR_MIPMAP_NEAREST", 4)
    glutAddMenuEntry(b"GL_LINEAR_MIPMAP_LINEAR", 5)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    SetupRC()
    glutMainLoop()
    ShutdownRC()

if __name__ == "__main__":
    main()
