# -*- coding: utf-8 -*-

"""
Created on Tue Nov 17 18:31:27 2015
@author: Richa
"""

import sys
INFINITY = sys.maxint


def print_neatly(words, M):
    """
    >>> print_neatly(['This','is','a','doctest'], 11)
    (64, 'This is\\na doctest')
    """
    """ Print text neatly.
    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file.
    M: int
        The max number of characters per line including spaces
    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters.
        It should not end with a blank line.
    Details
    -------
    Look at print_neatly_test for some code to test the solution.
    """
    words_total = len(words)
    text = ''

    (text_table, cost) = table_create(words, M)

    previous = words_total
    while previous >= 0:
        current = text_table[previous - 1]
        line = words[current]
        for j in range(current + 1, previous):
            line = line + ' ' + words[j]
        if previous != words_total:
            text = line + '\n' + text
        else:
            text = line

        previous = current

        if previous == 0:
            previous = -1

    return cost, text


def compute_least_cost(extras, words_total, index):
    val = 0
    if extras < 0:
        val = INFINITY
    elif index == words_total - 1 and extras >= 0:
        val = 0
    else:
        val = extras**3

    return val


def table_create(words, M):
    words_total = len(words)
    extras = [[0 for i in range(words_total)] for i in range(words_total)]
    least_cost = [[0 for i in range(words_total)] for j in range(words_total)]
    cost_table = [0 for i in range(0, words_total)]
    text_table = [0 for i in range(0, words_total)]

    for i in range(0, words_total):
        extras[i][i] = M - len(words[i])
        least_cost[i][i] = compute_least_cost(extras[i][i], words_total, i)
        for j in range(i + 1, words_total):
            extras[i][j] = extras[i][j - 1] - len(words[j]) - 1
            least_cost[i][j] = compute_least_cost(extras[i][j], words_total, j)

    for j in range(0, words_total):
        cost_table[j] = INFINITY
        for i in range(0, j):
            if (cost_table[i - 1] + least_cost[i][j]) < cost_table[j]:
                cost_table[j] = cost_table[i - 1] + least_cost[i][j]
                text_table[j] = i

    return text_table, cost_table[-1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
