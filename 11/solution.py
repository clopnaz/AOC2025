import itertools
import collections
import functools


@functools.cache
def get_paths(start='you', end='out'):
    # if start not in graph:
    #     pass
    # elif end in graph[start]:
    if end in graph[start]:
        return ((end,),)
    else:
        paths = []
        for s in graph[start]:
            got_paths = get_paths(start=s, end=end)
            if got_paths is not None:
                for path in got_paths:
                    paths.append((s,) + path)
        return tuple(paths)

memo1 = dict()
def reaches(loc):
    if loc in memo1:
        return memo1[loc]
    elif loc not in graph:
        memo1[loc] = ()
    else:
        memo1[loc] = []
        for newloc in graph[loc]:
            if newloc in ('fft', 'dac'):
                return (newloc,) + reaches(loc)
            else:
                return reaches(loc)
    return result

memo_two = dict()
def reaches_two(loc):
    # if loc in memo2:
        # yield memo2[loc]
    if loc not in memo_two:
        if loc not in graph:
            memo_two[loc] = {'dac': 0, 'fft': 0, 'out': 0}
        else:
            memo_two[loc] = {'dac': 0, 'fft': 0, 'out': 0}
            for newloc in graph[loc]:
                if newloc == 'dac':
                    memo_two[loc]['dac'] += 1
                elif newloc == 'fft':
                    memo_two[loc]['fft'] += 1
                elif newloc == 'out':
                    memo_two[loc]['out'] += 1
                else:
                    newout = reaches_two(newloc)
                    memo_two[loc]['dac'] += newout['dac']
                    memo_two[loc]['fft'] += newout['fft']
                    memo_two[loc]['out'] += newout['out']
    return memo_two[loc]

if __name__ == '__main__':
    txt = open('test.txt').read()
    # txt = open('input.txt').read()
    lines = txt.splitlines()
    graph = {x: y.strip().split(' ') for x,y in [l.split(':') for l in lines]}
    # print(graph)


    outs1 = list(get_paths())
    # for out in outs1:
    #     print(out)
    print(f"part 1: {len(outs1)}")



    txt = open('input.txt').read()
    txt = open('test2.txt').read()
    lines = txt.splitlines()
    graph = {x: y.strip().split(' ') for x,y in [l.split(':') for l in lines]}
    graph['out'] = ()
    svr_dests = reaches_two('svr')
    memo_two.clear()
    fft_dests = reaches_two('fft')
    memo_two.clear()
    dac_dests = reaches_two('dac')
    print(f"{svr_dests = }\n {fft_dests = }\n {dac_dests = }")
    print(svr_dests['dac'] * dac_dests['fft'] * fft_dests['out'])
    print(svr_dests['fft'] * fft_dests['dac'] * dac_dests['out'])
    # 367579641755680]


    breakpoint()
    part_2 = 0
    try:
        for out in outs2:
            print(out)
            if 'daq' in out and 'fft' in out:
                part_2 += 1
    except:
        breakpoint()
        pass
    print(part_2)
    breakpoint()



# for label in labels.items():
#     print(label)
# p1: just work backwards?
# reverse_counter = collections.defaultdict(list)
# for (start, ends) in graph.items():
#     for end in ends:
#         reverse_counter[end].append(start)
# for a, b in reverse_counter.items():
#     print(f"{a}: {b}")
