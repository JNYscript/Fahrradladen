import numpy as np


def get_levenshtein_distanz(s1, s2):
    size_x = len(s1) + 1
    size_y = len(s2) + 1

    m = np.zeros((size_x, size_y))
    for x in range(size_x):
        m[x, 0] = x
    for y in range(size_y):
        m[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if s1[x - 1] == s2[y - 1]:
                m[x, y] = min(m[x - 1, y] + 1, m[x - 1, y - 1], m[x, y - 1] + 1)
            else:
                m[x, y] = min(m[x - 1, y] + 1, m[x - 1, y - 1] + 1, m[x, y - 1] + 1)

    return m[size_x - 1, size_y - 1]


def get_all_substrings(length, search_String):
    if length > len(search_String):
        return [search_String]
    else:
        return [
            search_String[i : i + length]
            for i in range(0, len(search_String) - length + 1)
        ]


def get_levenshtein_distanze_substring(s1, s2):

    minimum = float("inf")

    sub_strings = get_all_substrings(len(s1), s2)

    for string in sub_strings:
        dis = get_levenshtein_distanz(s1, string)
        if dis < minimum:
            minimum = dis
        if dis == 0:
            break

    return minimum


def test():
    print(get_levenshtein_distanz("Haus", "Haus"))
    print(get_all_substrings(2, "ABCDE"))
    print(get_levenshtein_distanze_substring("bau", "Hausbau"))


if __name__ == "__main__":
    test()
