#!/usr/bin/env python3
import itertools
import functools

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
lines = txt.splitlines()
boxes = []
for line in lines:
    # print(line.split(','))
    boxes.append(tuple(map(int, line.split(','))))
boxset = set(boxes)
def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**.5

assert distance([0,0,0], [0,0,1]) == 1
assert distance([0,0,0], [0,0,10]) == 10
assert distance([4,0,0], [0,3,0]) == 5

ordered_connections = []
# for a in boxes:
#     for b in boxes:
#         distances.append((distance(a,b), (a, b)))
for a, b in itertools.combinations(boxes, 2):
    ordered_connections.append((distance(a,b), (a, b)))
ordered_connections.sort()
circuits = []
# for n in range(1000):
def merge():
    for a, b in itertools.combinations(range(len(circuits)), 2):
        circuit_a = circuits[a]
        circuit_b = circuits[b]
        if not circuit_a.isdisjoint(circuit_b):
            circuits[b].update(circuits.pop(a))
            return True
    return False

for new_connection in ordered_connections:
    # new_connection = ordered_connections[n]
    a, b = new_connection[1]
    for circuit in circuits:
        if a in circuit or b in circuit:
            circuit.update([a])
            circuit.update([b])
            break
    else:
        new_circuit = set()
        new_circuit.update((a,b))
        circuits.append(new_circuit)
    while merge():
        pass
    if len(circuits) == 1 and boxset == circuits[0]:
        break
print(f"part_2= {a[0] * b[0]}")
while merge():
    print('merge! ', end='')
    pass
# circuits.sort(key=len, reverse=True)
# print(len(circuits[0]) * len(circuits[1]) * len(circuits[2]))
breakpoint()
part_1 = 0
print(f"{part_1}")
