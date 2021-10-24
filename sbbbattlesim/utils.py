def get_support_targets(position, horn=False):
    if horn:
        return [1, 2, 3, 4]
    return {5: [1, 2], 6: [2, 3], 7: [3, 4]}.get(position, [])


def get_spawn_positions(position):
    spawn_order = {
        1: (1, 2, 3, 4, 5, 6, 7),
        2: (2, 3, 4, 1, 5, 6, 7),
        3: (3, 4, 2, 1, 5, 6, 7),
        4: (4, 3, 2, 1, 5, 6, 7),
        5: (5, 6, 7, 2, 1, 3, 4),
        6: (6, 7, 5, 3, 2, 1, 4),
        7: (7, 6, 5, 4, 3, 1, 2)
    }

    return spawn_order.get(position, ())