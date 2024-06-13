

def ordered_list_of_strings(input_data: list):

    n = len(input_data)
    output = [input_data[0]]

    for i in range(1, n):
        if len(input_data[i]) > len(output[-1]):

            output.append(input_data[i])
        else:

            low = 0
            high = len(output) - 1
            while low < high:
                mid = low + (high - low) // 2
                if output[mid] < input_data[i]:
                    low = mid + 1
                else:
                    high = mid

            output[low] = input_data[i]
    return len(output)
