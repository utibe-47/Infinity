from math import floor, ceil
Output = [24, 35, 9, 56, 12]


def swap(lst):
    input = lst.copy()
    first_element = input[0]
    input[0] = input[-1]
    input[-1] = first_element
    return input


def swap_first_last_3(input):
    if len(input) >= 2:
        output = input[-1:] + input[1:-1] + input[:1]
        return output
    return input


def swap_positions(_input, pos1, pos2):
    output = _input.copy()
    pos1_val, pos2_val = output[pos1 - 1], output[pos2 - 1]
    output[pos1 - 1], output[pos2 - 1] = pos2_val, pos2_val

    return output


def maximum(a, b):
    _max_lambda = lambda a, b: a if a > b else b
    _max = a if a > b else b
    return _max, _max_lambda


def symmetry_checker(string_input):
    size = len(string_input)
    if size % 2 > 0:
        raise AttributeError('Cannot be symmetrical')

    mid = size/2
    start = string_input[:mid]
    end_string = string_input[mid:]
    if start == end_string:
        return True
    elif start == end_string[::-1]:
        return False
    else:
        raise AttributeError('Neither')


def print_diamond(n):
    reverse_count = 0
    count = 0
    _string = '*'
    for i in range(n*2):
        if i < n:
            count += 1
        else:
            reverse_count += 1
            count = n - reverse_count
        print(_string * count)


def print_pyramid(n):
    if n % 2 > 0:
        star_ind = [(n + 1)/2 - 1]
    else:
        star_ind = [n/2 - 1, n/2]
    star_ind = list(map(int, star_ind))
    midpoint = star_ind[0]

    for i in range(n):
        if i > midpoint:
            break
        array = [' '] * n
        if i > 0:
            end_ind = star_ind[-1] + 1
            start_ind = star_ind[0] - 1
            star_ind.append(end_ind)
            star_ind.insert(0, start_ind)
        for ind in star_ind:
            array.insert(ind, '*')
        _str = ''.join(array)
        print(_str)


if __name__ == '__main__':
    print_pyramid(8)
    _input = [12, 35, 9, 56, 24]
    _output = swap(_input)
    _output2 = swap_first_last_3(_input)
    H = 8
