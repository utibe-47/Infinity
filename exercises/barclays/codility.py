

def solution(A):
    # Implement your solution here
    for i in range(len(A)):
        val = A[i]
        if val < 0:
            A[i] = '<'
        elif val == 0:
            A[i] = '='
        else:
            A[i] = '>'
    return ''.join(A)


def solution2(S):
    # Implement your solution here
    patch_count = 0
    counter = 0
    total_patches = 0
    for count in range(len(S)):
        val = S[count]
        if val == 'X':
            patch_count += 1
        counter +=1
        if counter == 3:
            if patch_count > 0:
                total_patches += 1
            counter = 0
            patch_count = 0
    if patch_count > 0 and counter < 3:
        total_patches += 1
    return total_patches


def solution3(A, F, M):
    # Implement your solution here
    roll = [1, 2, 3, 4, 5, 6]
    sum_a = sum(A)
    total_elements = len(A) + F
    total_sum = total_elements * M
    missing_sum = total_sum - sum_a
    if missing_sum < F:
        return [0]
    values = []

    def combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [0] * r

        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)

    for cc in combinations(roll, F):
        if sum(cc) == missing_sum:
            return list[cc]
    return [0]


def comb(iterable, n):
    _solution = [0]
    for i in range(len(iterable)):
        for j in reversed(range(len(iterable))):
            x, y = [iterable[i], iterable[j]]

            if x + y == n:
                _solution = [x, y]
                return _solution


if __name__ == '__main__':
    A = [3, 2, 4, 3]
    F = 2
    M = 4
    co = solution3(A, F, M)
    mm = list(co)
    dd = solution2(a)
