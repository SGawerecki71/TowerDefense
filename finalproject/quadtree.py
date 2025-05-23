import pygame

class Point:
    def __init__(self, x, y, obj):
        self.x = x
        self.y = y
        self.obj = obj

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, point):
        return (self.x <= point.x < self.x + self.w and
                self.y <= point.y < self.y + self.h)
    
    def intersects(self, circle_x, circle_y, radius):
    # Find the closest point on the rectangle to the circle center
        closest_x = max(self.x, min(circle_x, self.x + self.w))
        closest_y = max(self.y, min(circle_y, self.y + self.h))

    # Calculate distance from circle center to closest point
        dx = circle_x - closest_x
        dy = circle_y - closest_y

        return (dx * dx + dy * dy) <= (radius * radius)
    
class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h
        self.nw = Quadtree(Rectangle(x, y, w/2, h/2), self.capacity)
        self.ne = Quadtree(Rectangle(x + w/2, y, w/2, h/2), self.capacity)
        self.sw = Quadtree(Rectangle(x, y + h/2, w/2, h/2), self.capacity)
        self.se = Quadtree(Rectangle(x + w/2, y + h/2, w/2, h/2), self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            return (self.nw.insert(point) or self.ne.insert(point) or
                    self.sw.insert(point) or self.se.insert(point))

    def query_circle(self, x, y, radius, found):
        if not self.boundary.intersects(x, y, radius):
            return

        for p in self.points:
            dx = p.x - x
            dy = p.y - y
            if dx * dx + dy * dy <= radius * radius:
                found.append(p.obj)

        if self.divided:
            self.nw.query_circle(x, y, radius, found)
            self.ne.query_circle(x, y, radius, found)
            self.sw.query_circle(x, y, radius, found)
            self.se.query_circle(x, y, radius, found)