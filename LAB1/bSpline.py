import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width = 800
height = 800

V = []
F = []
krivulja_vrhovi = []
krivulja = []
tangente = []
os_rotacije = []
kut_rotacije = []

i = 0
B = 1/6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
dB = 1/2 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])

#početna orijentacija
s = np.array([0, 0, 1])


def ucitaj_objekt(objekt_file):
    with open(objekt_file, 'r') as file:
        for linija in file:
            linija = linija.rstrip().split(' ')
            if linija[0] == 'g':
                object_name = linija[1]
            if linija[0] == 'v':
                V.append([float(x) for x in linija[1:]])
            if linija[0] == 'f':
                F.append([int(x) for x in linija[1:]])


def ucitaj_krivulju(spline_file):
    with open(spline_file, 'r') as file:
        for linija in file:
            linija = linija.rstrip().split(' ')
            krivulja_vrhovi.append([int(x) for x in linija])


def izracunaj_krivulju():
    faktor = 0.8
    for n in range(0, len(krivulja_vrhovi) - 3):
        R = np.array([krivulja_vrhovi[n], krivulja_vrhovi[n + 1], krivulja_vrhovi[n + 2], krivulja_vrhovi[n + 3]])      #periodički segment
        for t in np.linspace(0, 1, 10):
            T = np.array([t*t*t, t*t, t, 1])
            P = np.dot(np.dot(T, B), R)            #točka  segmenta krivulje
            krivulja.append(P)

            dT = np.array([t*t, t, 1])
            dP = np.dot(np.dot(dT, dB), R)  # ciljna orijentacija
            tangenta = [P, P + faktor * dP]
            tangente.append(tangenta)       #parovi točki koji određuju tangente

            e = dP              #ciljna orijentacija
            os = np.cross(s, e)
            os_rotacije.append(os)
            kut = np.arccos(np.matmul(s, e) / (np.linalg.norm(s) * np.linalg.norm(e)))
            kut_rotacije.append(np.rad2deg(kut))


def crtaj_krivulju():
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    for segment in krivulja:
        glVertex3fv(segment)
    glEnd()

def crtaj_tangente():
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    for i in range(0, len(tangente)):
        glVertex3fv(tangente[i][0])
        glVertex3fv(tangente[i][1])
    glEnd()

def crtaj_objekt():
    global i
    skala = 4
    glColor(1, 1, 1)
    glTranslatef(krivulja[i][0], krivulja[i][1], krivulja[i][2])
    glRotatef(kut_rotacije[i], os_rotacije[i][0], os_rotacije[i][1], os_rotacije[i][2])

    if sys.argv[1] == 'teddy.obj':
        skala = 0.2
    if sys.argv[1] == 'avion.obj':
        skala = 10
    glScalef(skala, skala, skala)

    glBegin(GL_LINE_LOOP)
    for j in F:
        glVertex3fv((V[j[0] - 1]))
        glVertex3fv((V[j[1] - 1]))
        glVertex3fv((V[j[2] - 1]))
    glEnd()

    glutPostRedisplay()             #ponovno nacrtaj

def display():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    #resetiranje projekcije
    gluPerspective(70.0, float(width) / float(height), 0.0, 100.0)              #definiranje prikaza scene u prozoru
    glOrtho(-15.0, 15.0, -15.0, 15.0, 0.0, 50.0)                       #ortogonalna projekcija prikaza elemenata
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(-40, 1, 1, 0)
    glTranslatef(10, -20, 0)

    izracunaj_krivulju()

    crtaj_krivulju()
    crtaj_tangente()

    crtaj_objekt()

    glutSwapBuffers()           #promjena spremnik

def animate(x):
    global i
    i += 1
    if i == len(krivulja) - 1:
        i = 0
    glutTimerFunc(500, animate, 0)


def main():
    objekt = sys.argv[1]
    spline = sys.argv[2]

    ucitaj_objekt(objekt)
    ucitaj_krivulju(spline)

    glutInit()      #inicijalizacija biblioteke
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)        #način iscrtavanja scene - dva spremnika
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow('Racunalna animacija: Prva laboratorijska vjezba')

    glutDisplayFunc(display)            #poziv metode display u svrhu prikaza scene
    glutTimerFunc(500, animate, 0)
    glutMainLoop()

if __name__ == '__main__':
    main()
