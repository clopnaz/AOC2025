#!/usr/bin/env python3
import itertools

directions = []
directions.append([-1,0])
directions.append([+1,0])
directions.append([-1,-1])
directions.append([0,-1])
directions.append([+1,-1])
directions.append([-1,+1])
directions.append([0,+1])
directions.append([+1,+1])

# txt = open('test.txt').read()
txt = open('input.txt').read()
(fresh_ranges, available) = txt.split('\n\n')
class Range:
    def __init__(self, low, high):
        if low > high:
            (low,high) = (high,low)
        self.low = low
        self.high = high
        assert low <= high

    def overlaps(self, other):
        if self.low <= other.low <= self.high:
            return True
        if self.low <= other.high <= self.high:
            return True
        else:
            return False

    def join(self, other):
        if self.low < other.low:
            new_low = self.low
        else:
            new_low = other.low
        if self.high > other.high:
            new_high = self.high
        else:
            new_high = other.high
        self.low = new_low
        self.high = new_high

    def __contains__(self, ID):
        if self.low <= ID <= self.high:
            return True
        else:
            return False
    def __repr__(self):
        return f"{self.low}-{self.high}"
    
    def __len__(self):
        return self.high+1 - self.low

ranges = []
for idx, fresh_range in enumerate(fresh_ranges.splitlines()):
    (low,high) = map(int,fresh_range.strip().split('-'))
    new_range = Range(low,high)
    # print(f"{new_range}")
    for r in ranges:
        if r.overlaps(new_range):
            # print(f"joining {r} and {new_range}")
            r.join(new_range)
            # print(f"{r}")
            break
    else:
        ranges.append(new_range)
# reduce
keep_going = True
while keep_going:
    merged_ranges = []
    # print("START")
    # print(f"{ranges = }, {merged_ranges = }")
    keep_going = False
    for r_1 in ranges:
        for r_2 in merged_ranges:
            if r_1.overlaps(r_2):
                keep_going = True
                # print(f"joining {r_1} and {r_2}")
                r_2.join(r_1)
                break
        else:
            # print(f"append {r_1}")
            merged_ranges.append(r_1)
        # print(f"{merged_ranges}")
    # print(f"{ranges = }, {merged_ranges = }")
    ranges = merged_ranges
# for r in ranges:
#     print(f"{r = }")
part_1 = 0
for available_id in available.splitlines():
    available_id = int(available_id.strip())
    # print(f"{available_id = }")
    for r in ranges:
        # print(f"{r = }")
        if available_id in r:
            # print(f"{available_id = } is in {r}")
            part_1 += 1
            break
part_2 = 0
for r in ranges:
    part_2 += len(r)
    # print(f"{r = } {len(r) = }")

print(f"{part_1 = }")
print(f"{part_2 = }")
