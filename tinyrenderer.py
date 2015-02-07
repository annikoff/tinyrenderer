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
        self.zbuffer = []
        for i in range(self.width*self.height):
            self.zbuffer.append(-2147483648)

    def createImage(self):
        self.open('african_head.obj')
        lightDir = [0, 0, -1]
        for faces in self.faces:
            screenCoords = []
            worldCoords = []
            for i in range(len(faces)):
                x = (float(self.vertexes[int(faces[i])-1][0])+1.)*self.width/2
                y = (float(self.vertexes[int(faces[i])-1][1])+1.)*self.height/2
                z = (float(self.vertexes[int(faces[i])-1][2])+1.)*self.height/2
                screenCoords.append([int(round(x)), int(round(y)), int(round(z))])
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
                model.triangle(screenCoords[0][0], screenCoords[0][1], screenCoords[0][2],
                    screenCoords[1][0], screenCoords[1][1], screenCoords[1][2],
                    screenCoords[2][0], screenCoords[2][1], screenCoords[2][2],
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
        while 1:
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

    def rasterize(self, x0, y0, x1, y1, color, ybuffer):
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range(x0, x1):
            t = (x-x0)/float(x1-x0)
            y = int(y0*(1.0-t) + y1*t)
            if ybuffer[x] < y:
                ybuffer[x] = y
                self.draw.point((x, 0), color)

    def save(self):
        self.image.transpose(1).save("output.png", "PNG")

    def triangle(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, color):
        if y0 == y1 and y1 == y2:
            return
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if y0 > y2:
            x0, x2 = x2, x0
            y0, y2 = y2, y0
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        total_height = y2-y0;
        for i in range(total_height):
            second_half = (i>y1-y0) or (y1==y0)
            alpha =i/(total_height*1.0)
            ax = x0 + (x2-x0)*alpha
            ay = y0 + (y2-y0)*alpha
            az = z0 + (z2-z0)*alpha
            if second_half:
                segment_height = y2-y1
                beta = (i-(y1-y0))/(segment_height*1.0)
                bx = x1 + (x2-x1)*beta
                by = y1 + (y2-y1)*beta
                bz = z1 + (z2-z1)*beta
            else:
                segment_height = y1-y0
                beta = i/(segment_height*1.0)
                bx = x0 + (x1-x0)*beta
                by = y0 + (y1-y0)*beta
                bz = z0 + (z1-z0)*beta
            if ax > bx:
                ax, bx = bx, ax
            for j in range(int(ax), int(bx)):
                if ax == bx:
                    phi = 1.0
                else:
                    phi = (j-ax)/(bx-ax)
                px = ax +(bx-ax)*phi
                py = ay +(by-ay)*phi
                pz = az +(bz-az)*phi
                idx = int(px+py*self.width)
                if self.zbuffer[idx] < pz:
                    self.zbuffer[idx] = pz
                    self.draw.point((px, py), color)
                

if __name__ == '__main__':
    print 'Start'
    model = Model(800, 800)
    model.createImage()
    model.save()
    print 'Done'
