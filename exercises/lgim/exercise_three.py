from copy import deepcopy

import numpy as np


# Simplified Implementation to find ascending sub list using numpy
def find_ascending_sublist_numpy(words):
    word_count = list(map(len, words))
    output = max(np.split(words, np.where(np.diff(word_count) < 1)[0] + 1), key=len).tolist()
    return output


num2words_dict = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                  6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
                  11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
                  15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
                  19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
                  50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty',
                  90: 'Ninety', 0: 'Zero'}


def num2words(n: int) -> str:
    try:
        words = num2words_dict[n]
    except KeyError:
        try:
            words = num2words_dict[n - n % 10] + '-' + num2words_dict[n % 10].lower()
        except KeyError:
            raise KeyError('Number out of range')
    return words


def generate_word_list(numbers: list) -> list:
    numbers.sort()
    words = list(map(num2words, numbers))
    return words


def input_string_generator(input_data: list):
    for _string in input_data:
        yield _string


# More complex implementation to find the longest ascending sub list without using numpy or any packages
def find_increasing_sub_list(input_data: list) -> list:

    input_size = len(input_data)
    if input_size < 2:
        return input_data

    previous_string = input_data[0]
    primary_output = [previous_string]
    output_dict = {}

    for current_string in input_string_generator(input_data):
        if len(current_string) > len(previous_string):
            primary_output.append(current_string)
            previous_string = current_string
            if len(output_dict) > 0 and len(output_dict['primary_seq']) < len(primary_output):
                output_dict['primary_seq'] = primary_output
        else:
            previous_string = current_string
            if len(output_dict) == 0:
                output_dict['primary_seq'] = deepcopy(primary_output)
                primary_output = [previous_string]
            else:
                saved_seq = output_dict['primary_seq']
                if len(saved_seq) < len(primary_output):
                    output_dict['primary_seq'] = primary_output
                primary_output = [previous_string]

    if len(output_dict) > 0:
        return output_dict['primary_seq']
    else:
        return primary_output


if __name__ == '__main__':
    low, high = 10, 41
    _numbers = list(range(low, high + 1))
    _words = generate_word_list(_numbers)
    _output = find_increasing_sub_list(_words)
