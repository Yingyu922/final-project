


def naics_2_digit(group):
    m =list(group.io_naics.values)
    flat_list = [item for sublist in m for item in sublist]
    c_3 = set()
    for c_ in flat_list:
        c__ = c_.strip()
        c_3.add(c__[:2])
    return list(c_3)