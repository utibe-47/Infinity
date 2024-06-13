import numpy as np
import scipy as sp
from typing import Tuple


def generate_coordinates(nrows: int, ncolumns: int):
    for row in range(nrows):
        for column in range(ncolumns):
            yield row, column


def is_adjacent(row: int, column: int, new_row: int, new_column: int) -> bool:
    if row != new_row and column != new_column:
        return True
    return False


def chain_iterables(*iterables):
    for iterable in iterables:
        for element in iterable:
            yield element


def find_neighbours(row: int, column: int, nrows: int, ncolumns: int, found_nodes: dict) -> list:
    neighbour_rows = [row + x for x in range(-1, 2) if row + x != nrows and row + x >= 0]
    neighbour_cols = [column + x for x in range(-1, 2) if column + x != ncolumns and column + x >= 0]

    _neighbours = []
    for _row in neighbour_rows:
        for _column in neighbour_cols:
            if _row == row and _column == column:
                continue
            if is_adjacent(_row, _column, row, column):
                continue
            node_key = str(_row) + str(_column)
            if node_key in found_nodes:
                continue
            _neighbours.append((_row, _column))
    return _neighbours


def _find_child_neighbours(found_nodes: dict, input_array: np.ndarray, ncolumns: int, neighbours: list, node_count: int,
                           nrows: int) -> Tuple[int, dict, list]:
    _new_neighbour_list = []
    for _row, _column in neighbours:
        node_key = str(_row) + str(_column)
        if node_key in found_nodes:
            continue
        value = input_array[_row, _column]
        found_nodes[node_key] = value
        node_count += 1
        if value < 0.001:
            continue
        else:
            _new_neighbours: list = find_neighbours(_row, _column, nrows, ncolumns, found_nodes)
            _new_neighbour_list.extend(_new_neighbours)

    return node_count, found_nodes, _new_neighbour_list


def battleship_counter(input_array: np.ndarray) -> int:
    node_count, object_count = 0, 0
    found_nodes = {}
    nrows, ncolumns = input_array.shape
    n_nodes = nrows * ncolumns
    coordinates_generator = generate_coordinates(nrows, ncolumns)

    for row, column in coordinates_generator:
        if node_count == n_nodes:
            break
        node_key = str(row) + str(column)
        if node_key in found_nodes:
            continue

        node_count += 1
        value = input_array[row, column]
        found_nodes[node_key] = value
        if value < 0.001:
            continue
        else:
            neighbours: list = find_neighbours(row, column, nrows, ncolumns, found_nodes)
            if len(neighbours) == 0:
                object_count += 1
                continue
            all_neighbors_checked = False
            while not all_neighbors_checked:
                node_count, found_nodes, _new_neighbour_list = _find_child_neighbours(found_nodes, input_array,
                                                                                      ncolumns, neighbours, node_count,
                                                                                      nrows)
                if len(_new_neighbour_list) == 0:
                    all_neighbors_checked = True
                    object_count += 1
                else:
                    neighbours = _new_neighbour_list

    return object_count


if __name__ == '__main__':
    rng = np.random.default_rng()
    input_matrix = sp.sparse.random(5, 5, density=0.40, random_state=rng).toarray()
    number_of_ships = battleship_counter(input_matrix)
    print(number_of_ships)
