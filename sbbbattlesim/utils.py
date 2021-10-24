support_targets = {5: [1, 2], 6: [2, 3], 7: [3, 4]}


def get_support_targets(position, horn=False):
    if horn:
        return [1, 2, 3, 4]
    return support_targets.get(position, [])