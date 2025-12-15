#!/usr/bin/env python3
from __future__ import annotations
import itertools
import collections
import functools
import dataclasses

def apply_to_canonical_yx(fun):
    # I'm calling it canonical to have the center of the present be
    # (0,0). But I'm storing the presents with (0,0) as the top left.
    def canonicalized_function(yx, *args, **kwargs):
        yx = (yx[0] - 1, yx[1] - 1)
        yx = fun(yx, *args, **kwargs)
        yx = (yx[0] + 1, yx[1] + 1)
        return yx
    return canonicalized_function

@apply_to_canonical_yx
def rotated(yx, times):
    if times <= 0:
        return yx
    else:
        return rotated((yx[1], yx[0]), times - 1)

@apply_to_canonical_yx
def flipped(yx):
    return (-yx[0], yx[1])

@apply_to_canonical_yx
def mirrored(yx):
    return (yx[0], -yx[1])

@dataclasses.dataclass(frozen=True)
class Coords:
    y: int
    x: int
    t: int = 0 # theta: rotation
    vflip: int = 0
    hflip: int = 0

    def local2global(self, yx: tuple[int, int]):
            yx = rotated(yx, self.t)
            if self.hflip:
                yx = mirrored(yx)
            if self.vflip:
                yx = flipped(yx)
            yx = (yx[0] + self.x, yx[1] + self.y)
            return yx

    def locals2globals(self, yxs: list[tuple[int,int]]):
        return tuple(map(self.local2global, yxs))

next_present_unique_id = 0
def get_unique_present_id():
    global next_present_unique_id
    next_present_unique_id += 1
    return next_present_unique_id - 1


@dataclasses.dataclass
class Present:
    yxs: tuple[tuple[int,int]]
    unique_id: int = dataclasses.field(default_factory=get_unique_present_id)
    rotations: int = dataclasses.field(default_factory=get_unique_present_id)
    distinct_morphs: tuple[CoordsPresent] = dataclasses.field(init=False, repr=False)


    def __post_init__(self):
        moved_presents = []
        for rotation_amount in range(4):
            for hflip in [False, True]:
                for vflip in [False, True]:
                    moved_presents.append(self.moved(0, 0, rotation_amount, vflip, hflip))
        unique_yxs = set()
        breakpoint()
        self.disting_morphs
        for present in moved_presents:
            if present.yxs not in unique_yxs:
                pass





    @classmethod
    def fromstr(cls, string):
        indices = []
        for y, line in enumerate(string.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    indices.append((y,x))
        indices = tuple(indices)
        return cls(indices)

    def moved(self, *args, **kwargs):
        return CoordsPresent(self, Coords(*args, **kwargs))


@dataclasses.dataclass
class CoordsPresent():
    basepresent: Present
    coords: Coords

    @property
    def yxs(self):
        return self.coords.locals2globals(self.basepresent.yxs)
    @property
    def unique_id(self):
        return self.basepresent.unique_id

@dataclasses.dataclass
class Board:
    h: int
    w: int
    presentreqs: tuple[Present]
    presents: list[CoordsPresent] = dataclasses.field(default_factory=list)
    grid: list[int] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.grid = [[None for _ in range(self.w)] for _ in range(self.h)]

    @classmethod
    def from_text(cls, txt: str, presentshapes: tuple[Present]):
        a, b = map(str.strip, txt.split(":"))
        width, height = list(map(int, a.split('x')))
        presentreqs = list(map(int, b.split(' ')))
        return cls(height, width, presentreqs)

    def can_add(self, present: Present | CoordsPresent):
        for y, x in present.yxs:
            if self.grid[y][x] is not None:
                return False
        return True

    def add_present(self, present: Present | CoordsPresent):
        if not self.can_add(present):
            return False
        present_no = len(presents)
        for y, x in present.yxs:
            self.grid[y][x] = present.unique_id
        self.presents.append(present)
        return True

    def pop(self, index=-1):
        self.presents.pop(index)
        for y, x in present.yxs:
            assert self.grid[y][x] == present.unique_id




    def __str__(self):
        string = ''
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] is None:
                    string += '.'
                else:
                    string += str(self.grid[y][x])
            string += '\n'
        return string


def init(filename):
    txt = open(filename).read()
    txt_all_presents, _, txt_all_areas = txt.rpartition('\n\n')
    txt_presents = [a.split(':')[1].strip() for a in txt_all_presents.split('\n\n')]
    txt_areas = txt_all_areas.strip().split('\n')
    present_shapes = [Present.fromstr(x) for x in txt_presents]
    boards = [Board.from_text(x, present_shapes) for x in txt_areas]
    return present_shapes, boards

if __name__ == '__main__':
    presents, boards = init('input.txt')
    board = boards[0]
    present = presents[0]
    board.add_present(presents[1].moved(0,0))
    board.add_present(presents[0].moved(3,0))
    board.add_present(presents[2].moved(0,3))
    print(f"{board.presents[0].yxs = }")
    print(f"{board.presents[1].yxs = }")
    print(f"{board = }")
    print(boards[0])
    breakpoint()
