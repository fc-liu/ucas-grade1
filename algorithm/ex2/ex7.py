'''
:parameter
l: the sequence of numbers
i: current index
n: total numbers of the sequence
max: the list record the max length of every entry
seq: the max length sequence of every entry
last_max: the global max length sequence index
'''


def max_seq(l, i, n, max, seq, last_max):
    if i >= n:
        return last_max
    elif i == 0:
        max.append(1)
        seq.append([l[0]])
        i += 1
        return max_seq(l, i, n, max, seq, 0)
    else:
        max.append(0)
        seq.append([])
        '''
        for every entry beyond i, count max(i)=max(max(i),max(j)+1)
        '''
        for j in range(0, i):
            sub_seq = seq[j].copy()
            last = sub_seq[sub_seq.__len__() - 1]
            if last < l[i]:
                if max[i] > max[j] + 1:  # don't need update
                    continue
                else:  # update max[] and seq[]
                    max[i] = max[j] + 1
                    sub_seq.append(l[i])
                    seq[i] = sub_seq
        if max[last_max] > max[i]:
            return max_seq(l, i + 1, n, max, seq, last_max)
        else:
            return max_seq(l, i + 1, n, max, seq, i)


"""
:parameter
l: the input list of numbers
"""


def max_length(l):
    max = []
    seq = []
    i = 0
    n = l.__len__()
    ind = max_seq(l, i, n, max, seq, 0)
    return seq[ind]


if __name__ == '__main__':
    l = [1, 2, 5, 6, 432, 3, 4, 7, 4]
    sub_l = max_length(l)
    print(sub_l)
