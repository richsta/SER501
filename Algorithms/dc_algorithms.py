# -*- coding: utf-8 -*-

"""
Created on Tue Sep 15 18:31:27 2015
@author: Richa
"""

from numpy import *

"""STOCK_PRICES  = [100,113,110,85,105,102,
86,63,81,101,94,106,101,79,94,90,97]"""
STOCK_PRICE_CHANGES = [13, - 3, - 25, 20, - 3, - 16,
                       - 23, 18, 20, - 7, 12, - 5, - 22, 15, - 4, 7]


def find_maximum_subarray_brute(A, low=0, high=-1):                 # The maximum subarray brute force solution.
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.          # Doctest
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10, 43)
    """
    leftindex = 0
    rightindex = 0
    neg = float("inf")
    maxsum = -neg                                          # Initializing the maximum sum to infinity
    for i in range(low, high):                          # Iteration of for loop from low to high
        sum = 0
        for j in range(i, high):                        # Iteration of for loop from i to high
            sum += A[j]
            if sum > maxsum:                               # Comparing sum against the maximum sum
                maxsum = sum
                rightindex = j
                leftindex = i
    return leftindex, rightindex, maxsum                    # Return a tuple (i,j, max sum) where A[i:j] is the maximum subarray.


def find_maximum_crossing_subarray(A, low, mid, high):          #The maximum subarray crossing solution
    """
    Find the maximum subarray that crosses mid                          # Doctest
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    >>> find_maximum_crossing_subarray(STOCK_PRICE_CHANGES, 0, 8, 15)
    (7, 10, 43)
    """
    neg = float("inf")
    leftsum = -neg                                              # Initializing the left array sum to infinity
    sum = 0
    maxleft = 0
    maxright = 0
    for i in xrange(mid, low, - 1):                             # Iteration of reverse for loop in the left hand side array
        sum = sum + A[i]
        if sum > leftsum:                                       # Comparing the sum against right sum
            leftsum = sum
            maxleft = i
    rightsum = -neg                                             # Initializing the left array sum to infinity
    sum = 0
    for j in range(mid+1, high):                                # Iteration of for loop in the right hand side array
        sum = sum + A[j]
        if sum > rightsum:                                         # Comparing the sum against right sum
            rightsum = sum
            maxright = j
    return maxleft, maxright, leftsum + rightsum      # Return a tuple (i,j, left + right sum) where A[i:j] is the maximum subarray.


def find_maximum_subarray_recursive(A, low=0, high=-1):             # The maximum subarray recursive solution
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.              # Doctest
    Recursive method from chapter 4
    >>> print find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10, 43)
    """
    if high is low:                                                 # If length of array is 1
        return low, high, A[low]
    else:
        mid = (low+high)/2
        leftlow, lefthigh, leftsum = \
            find_maximum_subarray_recursive(A, low, mid)            # Recursive funtion
        rightlow, righthigh, rightsum = \
            find_maximum_subarray_recursive(A, mid+1, high)            # Recursive funtion
        crosslow, crosshigh, crosssum = \
            find_maximum_crossing_subarray(A, low, mid, high)           # Recursive funtion invoking maximum crossing subarray
        if leftsum >= rightsum & leftsum >= crosssum:
            return leftlow, lefthigh, leftsum               # Return a tuple (i,j, leftsum) where A[i:j] is the maximum subarray.
        elif rightsum >= leftsum & rightsum >= crosssum:
            return rightlow, righthigh, rightsum            # Return a tuple (i,j, rightsum) where A[i:j] is the maximum subarray.
        else:
            return crosslow, crosshigh, crosssum         # Return a tuple (i,j, crosssum) where A[i:j] is the maximum subarray.


def find_maximum_subarray_iterative(A, low=0, high=-1):                 # The maximum subarray iterative solution
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.              # Doctest
    Do problem 4.1-5 from the book.
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, 15)
    (7, 10, 43)
    """
    neg = float("inf")
    maxsum = -neg                                                   # Initializing the maximum sum to infinity
    maxleft = low
    maxright = low
    sum = low
    leftindex = low
    rightindex = low
    for i in range(low, high):                                  # For loop iteration from low to high
        sum = sum + A[i]
        if sum > maxsum:                                        # Comparing sum to the maximum sum
            maxsum = sum
            rightindex = i
            maxleft = leftindex
            maxright = rightindex
        elif sum < 0:                                           # Re initializing sum to 0
            sum = 0
            leftindex = i + 1
            rightindex = i + 1

    return maxleft, maxright, maxsum                     # Return a tuple (i,j, maximum sum) where A[i:j] is the maximum subarray.


X = [[2, 3], [3, 5]]                                        # Sample matrices
Y = [[1, 2], [5, -1]]
C = [[0, 0], [0, 0]]


def square_matrix_multiply(A, B):                              # Square matrix multiplication with O(n^3) complexity
    """
    Return the product AB of matrix multiplication.                     # Doctest
    >>> square_matrix_multiply([[2,3],[3,5]],[[1,2],[5,-1]])
    [[17, 1], [28, 1]]
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape                                # Asserting that dimensions of matrix A and B are equal
    assert A.shape == A.T.shape                             # Asserting that dimensions of matrix A and traspose of matrix B is equal

    for i in range(0, A.shape[0]):                          # For loop iteration from 0 to length of matrix A
        for j in range(0, B.shape[1]):
            C[i][j] = 0
            for k in range(0, B.shape[0]):
                C[i][j] = C[i][j] + (A[i][k] * B[k][j])
    return C                                                    # Returns the multiplied matrix


def divide_matrix(A):                                           # Dividing the matrix into 4 parts for Strassens's multiplication
    n = A.shape[0]
    A11 = A[ix_(range(0, n/2), range(0, n/2))]                  # ix function is used for indexing integers
    A12 = A[ix_(range(0, n/2), range(n/2, n))]
    A21 = A[ix_(range(n/2, n), range(0, n/2))]
    A22 = A[ix_(range(n/2, n), range(n/2, n))]
    return (A11, A12, A21, A22)


def square_matrix_multiply_strassens(A, B):                                   # Strassen's multiplication function
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    >>> square_matrix_multiply_strassens([[2, 3], [3, 5]], [[1, 2], [5, -1]])           #Doctest
    [[17, 1], [28, 1]]
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"

    n = A.shape[0]

    if n == 1:                                                          # Checking for the base case of recursion
        a = zeros(shape=(1, 1), dtype = int)
        a[0][0] = A[0][0] * B[0][0]
        return a

    (A11, A12, A21, A22) = divide_matrix(A)
    (B11, B12, B21, B22) = divide_matrix(B)

    S1 = (B12 - B22)                                                    #  Strassen's computations
    S2 = (A11 + A12)
    S3 = (A21 + A22)
    S4 = (B21 - B11)
    S5 = (A11 + A22)
    S6 = (B11 + B22)
    S7 = (A12 - A22)
    S8 = (B21 + B22)
    S9 = (A11 - A21)
    S10 = (B11 + B12)

    P1 = square_matrix_multiply_strassens(A11, S1)
    P2 = square_matrix_multiply_strassens(S2, B22)
    P3 = square_matrix_multiply_strassens(S3, B11)
    P4 = square_matrix_multiply_strassens(A22, S4)
    P5 = square_matrix_multiply_strassens(S5, S6)
    P6 = square_matrix_multiply_strassens(S7, S8)
    P7 = square_matrix_multiply_strassens(S9, S10)
    C11 = (P5 + P4 + P6) - P2
    C12 = P1 + P2
    C21 = P3 + P4
    C22 = P5 + P1 - P3 - P7
    C = zeros(shape=(n, n), dtype = int)

    C1 = concatenate((C11, C12), axis=1)
    C2 = concatenate((C21, C22), axis=1)
    C = concatenate((C1, C2), axis=0)

    return C.tolist()                                       # Returns array C as a list


def test():
    print find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, 15)
    print find_maximum_crossing_subarray(STOCK_PRICE_CHANGES, 0, 8, 15)
    print find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, 15)
    print find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, 15)
    print square_matrix_multiply(X, Y)
    print square_matrix_multiply_strassens([[2, 3], [3, 5]], [[1, 2], [5, -1]])


if __name__ == '__main__':
    test()
    import doctest
    doctest.testmod()
