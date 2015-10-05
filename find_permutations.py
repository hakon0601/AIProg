


def one_segment_permutations(segments, segment_index, list_size):
    if segment_index == len(segments):
        return [[]]
    segment_size = segments[segment_index]
    if segment_size > list_size:
        return -1
    permutations = []
    for i in range(list_size):
        if i + segment_size <= list_size:
            perm = [False for j in range(i)]
            for k in range(i, i + segment_size):
                perm.append(True)
            print str(perm)
            more_permutations = one_segment_permutations(segments, segment_index=segment_index+1, list_size=list_size-(k+1+1))
            if more_permutations == -1:
                continue
            for p in more_permutations:
                if len(p) > 0:
                    new_perm = perm + [False] + p
                else:
                    new_perm = perm
                permutations.append(new_perm)
    return permutations


dim = 10
permutations = one_segment_permutations(segments=[1, 1, 3], segment_index=0, list_size=dim)
for perm in permutations:
    if len(perm) != dim:
        perm += [False for i in range(dim - len(perm))]
print str(permutations)
