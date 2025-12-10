#!/usr/bin/env python3

from __future__ import annotations

import itertools
import functools
import dataclasses
from multiprocessing import Pool
# import matplotlib
# from matplotlib import pyplot

directions = []
directions.append([-1,0])
directions.append([+1,0])
directions.append([-1,-1])
directions.append([0,-1])
directions.append([+1,-1])
directions.append([-1,+1])
directions.append([0,+1])
directions.append([+1,+1])

# squares = [(x,y) for (x,y) in line.strip().split() for line in lines]

def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**.5

def get_area(a,b):
    return (1 + abs(b[1] - a[1]))*(1 + abs(b[0] - a[0]))

#  . a . d . 1
#  . . . . . 2
#  . c . b . 3
#  1 2 3 4 5
# a = 1 2
# b = 3 4
# c = 3 2 = (b[0] a[1])
# d = 1 4 = (a[0] b[1])


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise(IndexError(key))

    @functools.cached_property
    def list(self):
        return [self.x, self.y]

    def is_on(self, other: Segment):
        return other.contains(self) or self in (other.a, other.b)

@dataclasses.dataclass
class Segment:
    a: Point
    b: Point

    def __post_init__(self):
        try:
            assert any(self.direction) and not all(self.direction)
        except:
            breakpoint()
            pass

    @functools.cached_property
    def list(self):
        return [self.a.list, self.b.list]

    @functools.cached_property
    def direction(self):
        direction = [self.b[0]-self.a[0], self.b[1]-self.a[1]]
        for n in range(len(direction)):
            if direction[n]:
                direction[n] = direction[n] // abs(direction[n])
        return tuple(direction)

    @functools.cached_property
    def norm(self):
        return (-self.direction[1], self.direction[0])

    def contains(self, other: Point):
        if self.direction[0]:
            var_idx = 0
            const_idx = 1
        else:
            var_idx = 1
            const_idx = 0
        return (
                (
                    self.a[var_idx] < other[var_idx] < self.b[var_idx] or
                    self.a[var_idx] > other[var_idx] > self.b[var_idx]
                ) and (
                    self.a[const_idx] == other[const_idx]
                ))

    def intersects(self, other: Point):
        # . . . . . . . . . . .
        # . . . . . . . . . . .
        # . . . | . . . . . . .
        # . - - - - - . . . . .
        # . . . | . . . . . . .
        # . . . | . . . . . . .
        # . . . . . . . . . . .
        # . . . . . . . . . . .
        # a = 1,4
        # b = 5,4
        # a = 3,2
        # b = 3,5

        if self.direction == other.direction:
            return False
        if self.direction[0]:
            possible_cross = Point(other.a[0], self.a[1])
        else:
            possible_cross = Point(self.a[0], other.a[1])
        return (self.contains(possible_cross) and other.contains(possible_cross))

    @property
    def line_collection(self):
        return matplotlib.collections.LineCollection([[self.a.list, self.b.list]])

test1_line = Segment(a=Point(x=97554, y=50097), b=Point(x=97735, y=50097))
test1_point = Point(x=59707, y=50097)
assert not test1_line.contains(test1_point)
tseg_rect = Segment(a=Point(x=59707, y=2784), b=Point(x=59707, y=97183))
tseg_poly = Segment(a=Point(x=97554, y=50097), b=Point(x=97735, y=50097))
assert not tseg_rect.intersects(tseg_poly)
assert not tseg_poly.intersects(tseg_rect)
p1 = Point(0,1)
p2 = Point(10,1)
p1p2 = Segment(p1,p2)
p3 = Point(5,1)
p4 = Point(2,9)
p5 = Point(9,2)
assert p1.is_on(p1p2)
assert p2.is_on(p1p2)
assert not p1p2.contains(p1)
assert not p1p2.contains(p2)
assert p1p2.contains(p3)
assert not p1p2.contains(p4)
assert not p1p2.contains(p5)


@dataclasses.dataclass
class Polygon:
    segments: list(Segment)

    @functools.cached_property
    def points(self):
        points = set()
        for segment in self.segments:
            for point in segment.list:
                points.update([Point(point[0], point[1])])
        return points

    @functools.cached_property
    def point_combinations(self):
        return tuple(itertools.combinations(self.points, 2))

    def __iter__(self):
        return iter(self.segments)

    def covers(self, other: Rectangle):
        for point in self.points:
            if other.contains(point):
                return False
        for rect_segment in other.segments:
            for poly_segment in self.segments:
                if rect_segment.intersects(poly_segment):
                    # ax = pyplot.gca()
                    # c0 = other.line_collection
                    # c0.set_color('black')
                    # c0.set_linewidth(0.5)
                    # ax.add_collection(c0)
                    # c1 = poly_segment.line_collection
                    # c1.set_color('green')
                    # c1.set_linewidth(5)
                    # ax.add_collection(c1)
                    # c2 = rect_segment.line_collection
                    # c2.set_color('red')
                    # c2.set_linewidth(1)
                    # ax.add_collection(c2)
                    # ax.plot([other.p1.list, other.p2.list], color='magenta', marker='o')
                    # breakpoint()
                    return False
        return True



@dataclasses.dataclass
class Rectangle:
    p1: Point
    p2: Point

    @functools.cached_property
    def area(self):
        return get_area(self.p1, self.p2)

    def __lt__(self, other):
        return self.area < other.area

    def __gt__(self, other):
        return self.area > other.area

    def __eq__(self, other):
        return self.area == other.area

    def contains(self, other: Point):
        return (
                    self.p1[0] < other[0] < self.p2[0]
                    or self.p1[0] > other[0] > self.p2[0]
                ) and (
                    self.p1[1] < other[1] < self.p2[1]
                    or self.p1[1] > other[1] > self.p2[1]
                )

    @functools.cached_property
    def pa(self):
        return Point(self.p1[0], self.p2[1])

    @functools.cached_property
    def pb(self):
        return Point(self.p2[0], self.p1[1])

    @property
    def segments(self):
        return [
                Segment(self.p1, self.pa),
                Segment(self.pa, self.p2),
                Segment(self.p2, self.pb),
                Segment(self.pb, self.p1),
                ]
    @property
    def line_collection(self):
        l = [s.list for s in self.segments]
        return matplotlib.collections.LineCollection(l, linewidths=2)


if __name__ == '__main__':
    # txt = open('test.txt').read()
    txt = open('input.txt').read()
    lines = txt.splitlines()
    polygon_points = []
    x_vals = []
    y_vals = []
    for line in lines:
        x,y = map(int,line.strip().split(','))
        x_vals.append(x)
        y_vals.append(y)
        polygon_points.append(Point(x,y))
    x_floor = min(x_vals) - 1
    y_floor = min(y_vals) - 1

    polygon_segments = []
    for i in range(len(polygon_points)):
        j = i-1
        polygon_segments.append(Segment(polygon_points[i], polygon_points[j]))
    polygon = Polygon(polygon_segments)

    linelist = [s.list for s in polygon]
    # plotlines = matplotlib.collections.LineCollection(linelist, linewidths=2)
    # print(plotlines)
    # fig = matplotlib.pyplot.figure(1)
    # fig.gca().add_collection(plotlines)
    # fig.show()
    # fig.gca().set_xlim(1000,99999)
    # fig.gca().set_ylim(1000,99999)
    rectangles = []
    for p1, p2 in polygon.point_combinations:
        if p1[0] == p2[0]:
            continue
        if p1[1] == p2[1]:
            continue
        rectangles.append(Rectangle(p1, p2))
    rectangles.sort(reverse=True)
    test_rect1 = Rectangle(p1=Point(x=94969, y=48695), p2=Point(x=3910, y=37965))
    test_rect2 = Rectangle(p1=Point(x=32340, y=5390), p2=Point(x=98064, y=46468))
    test_point2 = Point(76614, 10885)
    # fig.gca().add_collection(test_rect2.line_collection)
    assert test_rect2.contains(test_point2)
    assert not polygon.covers(test_rect2)
    assert polygon.covers(test_rect1)
    print(len(rectangles))
    for rectangle in rectangles:
        if [94969, 48695] in (rectangle.p1.list, rectangle.p2.list):
            if [3910, 37965] in (rectangle.p1.list, rectangle.p2.list):
                fig.gca().add_collection(rectangle.line_collection)
                # breakpoint()
        if polygon.covers(rectangle):
            print(rectangle)
            print(rectangle.area)
            exit()
            fig.gca().add_collection(rectangle.line_collection)


    breakpoint()
    # 1428829072
    # 1301836184
    # 1396494456
    areas.sort()
    areas2.sort()

    print(areas[-1])
    print(areas2[-1])
    breakpoint()
