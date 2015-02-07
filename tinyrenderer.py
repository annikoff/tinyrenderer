#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import random
import math

def pow_with_nan(x, y):
    try:
        return math.pow(x, y)
    except ValueError:
        return float(0)

class Model:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), (0,0,0))
        self.draw = ImageDraw.Draw(self.image)
        self.vertexes = []
        self.faces = []

    def createImage(self):
        self.open('african_head.obj')
        lightDir = [0, 0, -1]
        for faces in self.faces:
            screenCoords = []
            worldCoords = []
            for i in range(len(faces)):
                x = (float(self.vertexes[int(faces[i])-1][0])+1.)*self.width/2
                y = (float(self.vertexes[int(faces[i])-1][1])+1.)*self.height/2
                screenCoords.append([int(round(x)), int(round(y))])
                worldCoords.append([self.vertexes[int(faces[i])-1][0], self.vertexes[int(faces[i])-1][1], self.vertexes[int(faces[i])-1][2]])
            vx1 = float(worldCoords[0][0]) - float(worldCoords[1][0])
            vy1 = float(worldCoords[0][1]) - float(worldCoords[1][1])
            vz1 = float(worldCoords[0][2]) - float(worldCoords[1][2])
            vx2 = float(worldCoords[1][0]) - float(worldCoords[2][0])
            vy2 = float(worldCoords[1][1]) - float(worldCoords[2][1])
            vz2 = float(worldCoords[1][2]) - float(worldCoords[2][2])
            N = []
            N.append(vy1 * vz2 - vz1 * vy2) 
            N.append(vz1 * vx2 - vx1 * vz2) 
            N.append(vx1 * vy2 - vy1 * vx2)
            wrki = math.sqrt(math.pow(vy1*vz2-vz1*vy2, 2)+math.pow(vz1*vx2-vx1*vz2, 2)+math.pow(vx1*vy2-vy1*vx2, 2)) 
            N[0] = N[0] / wrki 
            N[1] = N[1] / wrki 
            N[2] = N[2] / wrki
            n = N[0]*lightDir[0] + N[1]*lightDir[1] + N[2]*lightDir[2]
            n *= -1
            if n > 0:
                model.triangle(screenCoords[0][0], screenCoords[0][1], 
                    screenCoords[1][0], screenCoords[1][1], 
                    screenCoords[2][0], screenCoords[2][1],
                    (int(n*255), int(n*255), int(n*255)))
        self.save()

    def open(self, filename):
        f = open(filename, 'r')
        for line in f:
            lineArr = line.strip("\n").split(" ")
            if lineArr[0] == "v":
                self.vertexes.append(lineArr[1:])
            elif lineArr[0] == "f":
                f = []
                faceArr = [lineArr[1], lineArr[2], lineArr[3]]
                for face in faceArr:
                    f.append(face.split("/")[0])
                self.faces.append(f)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1-x0)
        if x0 < x1:
            sx = 1
        else:
            sx = -1
        dy = abs(y1-y0)
        if y0 < y1:
            sy = 1
        else:
            sy = -1
        if dx > dy:
            err = dx
        else:
            err = -dy
        err = int(err/2.0)
        line = []
        while True:
            self.draw.point((x0, y0), color)
            line.append([x0, y0])
            if x0 == x1 and y0 == y1:
                break
            e2 = err;
            if e2 > -dx:
                err -= dy
                x0 += sx
            if e2 < dy:
                err += dx
                y0 += sy
        return line

    def save(self):
        self.image.transpose(1).save("output.png", "PNG")

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if y0 > y2:
            x0, x2 = x2, x0
            y0, y2 = y2, y0
        firstLine = self.line(x0, y0, x1, y1, color)
        secondLine = self.line(x2, y2, x0, y0, color)
        for i in firstLine:
            for j in secondLine:
                self.line(i[0], i[1], j[0], j[1], color)

if __name__ == '__main__':
    print 'Start'
    model = Model(800, 800)
    model.createImage()
    #model.triangle(10, 70, 50, 160, 70, 80, '#FF00FF')
    #model.triangle(180, 50, 150, 1, 70, 180, '#FFFFFF')
    #model.triangle(180, 150, 120, 160, 130, 180, '#FF0000')
    model.save()
    print 'Done'
