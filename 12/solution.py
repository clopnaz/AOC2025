import itertools
import collections
import functools
import dataclasses
import matplotlib.pyplot

@dataclasses.dataclass(frozen=True)
class Morph:
    rotations: int
    mirror: int
    flip: int
    @property
    def fun(self):
        def fun(index):
            if self.rotations:
                index = rotated(index, self.rotations)
            if self.mirror:
                index = mirrored(index)
            if self.flip:
                index = flipped(index)

@dataclasses.dataclass(frozen=True)
class Present:
    indices: frozenset[tuple[int]]

    @classmethod
    def fromstr(cls, string):
        indices = []
        for y, line in enumerate(string.splitlines()):
            for x, char in enumerate(line):
                if char == '#':
                    indices.append((y,x))
        indices = tuple(indices)
        return cls(indices)

    @classmethod
    def fromints(cls, ints):
        strs = [f"{i:03b}" for i in ints]
        string = '\n'.join(map(lambda x: x.replace('0', '.').replace('1','#'), strs))
        return cls.fromstr(string)

    @functools.cached_property
    def complexity(self):
        return len(self.all_transforms())
    @functools.cached_property
    def ints(self):
        a = 0
        ints = []
        for line in str(self).splitlines():
            ints.append(int(line.replace('.', '0').replace('#','1'), 2))
        return ints

    def __lt__(self, other):
        # sort more complex first
        return self.complexity > other.complexity

    def __eq__(self, other):
        return self.indices == other.indices

    def __str__(self):
        stringlist = [['.']*3 for _ in range(3)]
        for y, x in self.indices:
            stringlist[y][x] = '#'
        string = '\n'.join([''.join(s) for s in stringlist])
        return string

    @functools.cache
    def indices_offs(self, yoffs=0, xoffs=0):
        return tuple([(y+yoffs, x+xoffs) for y,x in self.indices])


    def plotXY(self, yoffs=0, xoffs=0):
        Y, X = zip(*self.indices_offs(yoffs, xoffs))
        return X, Y

    def apply(self, fun, *args, **kwargs):
       return Present(frozenset([fun(idx, *args, **kwargs) for idx in self.indices]))

    @functools.cached_property
    def all_morphs(self) -> list[Morph]:
        present2morph = dict()
        for num_rotations in range(4):
            for do_flip in [False, True]:
                for do_mirror in [False, True]:
                    morph = Morph(num_rotations, do_mirror, do_flip)
                    morphed_present = self.apply(morph.fun)
                    if morphed_present not in present2morph:
                        present2morph[morphed_present] = morph
        return tuple(present2morph.values)





def canonicalize(fun):
    def new_fun(index, *args, **kwargs):
        index = (index[0] - 1, index[1] - 1)
        index = fun(index, *args, **kwargs)
        index = (index[0] + 1, index[1] + 1)
        return index
    return new_fun

@canonicalize
def rotated(index, times):
    if times <= 0:
        return index
    else:
        return rotated((index[1], index[0]), times - 1)

@canonicalize
def flipped(index):
    return -index[0], index[1]

@canonicalize
def mirrored(index):
    return (index[0], -index[1])

@canonicalize
def canoned(index):
    return index[0] - 1, index[1] - 1

@canonicalize
def uncanoned(index):
    return index[0] + 1, index[1] + 1

@dataclasses.dataclass(frozen=True)
class Pos:
    x: int
    y: int
    @property
    def fun(self):
        def fun(index):
            index = (index[0]+self.x, index[1]+self.y)
        return fun



@dataclasses.dataclass
class Area:
    height: int
    width: int
    presents: list[Present]
    present_demands: list[int]
    present_grid: list[list[int]] = dataclasses.field(init=False)
    present_count: dict[int, int] = dataclasses.field(init=False)
    present_locations: list[int, Morph] = dataclasses.field(init=False)

    @classmethod
    def from_text(cls, txt: str, presents: list[Present]):
        a, b = map(str.strip, txt.split(":"))
        width, height = list(map(int, a.split('x')))
        present_demands = list(map(int, b.split(' ')))
        return cls(height, width, presents, present_demands)

    @property
    def area(self):
        return self.width * self.height

    @property
    def naive_possible(self):
        return self.area_demanded > self.area

    @property
    def area_demanded(self):
        total = 0
        for present_demand in self.present_demands:
            total += present_demand * 7
        return(total)

    @property
    def satisfied(self):
        res = True
        for presentno in range(len(self.present_demands)):
            if self.present_demands[presentno] != self.present_count[presentno]:
                res = False
        return res

    def insert(self, present_no: int, loc: Morph, ):
        self.present_count[present_no] += 1
        self.present_locations.append((present_no, location))

    def can_insert(self, present_no: int, loc: Morph):
        pass






def init(filename):
    txt = open(filename).read()
    txt_all_presents, _, txt_all_areas = txt.rpartition('\n\n')
    txt_presents = [a.split(':')[1].strip() for a in txt_all_presents.split('\n\n')]
    txt_areas = txt_all_areas.strip().split('\n')
    presents = [Present.fromstr(x) for x in txt_presents]
    for present in presents:
        assert Present.fromints(present.ints) == present
    areas = [Area.from_text(x, presents) for x in txt_areas]
    return presents, areas


if __name__ == '__main__':
    # presents, areas = init('test.txt')
    presents, areas = init('input.txt')
    # let's just try to put some together
    max_gcd = -1
    for area in areas:
        # print(area.possible)
        if area.naive_possible:
            area.gcd = None
            for divisor in range(1,min(area.present_demands)+1):
                if sum(map(lambda x: x % divisor == 0, area.present_demands)) > 4:
                    area.gcd = divisor
                    max_gcd = max(max_gcd, divisor)
    print(max_gcd)
    breakpoint()


