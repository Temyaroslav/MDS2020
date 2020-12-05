from copy import deepcopy

class MatrixSizeError(Exception):
    pass

class Matrix:
    # Part 1
    def __init__(self, matrix):
        self.matrix = deepcopy(matrix)

    def __str__(self):
        s = ''
        for row in self.matrix:
            for col in row:
                s += f'{col}\t'
            s = s[:-1]
            s += '\n'
        return s[:-1]

    @staticmethod
    def __check_type(other):
        if not isinstance(other, Matrix):
            raise TypeError
        return

    def __check_size(self, other):
        if self.size() != other.size():
            raise MatrixSizeError
        return

    # Part 2
    def __eq__(self, other):
        self.__check_type(other)
        if self.size() != other.size():
            return False
        else:
            return self.matrix == other.matrix

    def size(self):
        return (len(self.matrix), len(self.matrix[0]))

    # Part 3
    def __add__(self, other):
        self.__check_type(other)
        self.__check_size(other)
        for row1, row2 in zip(self.matrix, other.matrix):
            for i in range(len(row1)):
                row1[i] += row2[i]
        return self

    def __sub__(self, other):
        self.__check_type(other)
        self.__check_size(other)
        for row1, row2 in zip(self.matrix, other.matrix):
            for i in range(len(row1)):
                row1[i] -= row2[i]
        return self

    # Part 4
    def __mul__(self, other):
        self.__check_type(other)
        if self.size()[1] != other.size()[0]:
            raise MatrixSizeError
        other = other.transpose()
        mx = []
        for row1 in self.matrix:
            new_row = []
            for row2 in other.matrix:
                s = 0
                for x, y in zip(row1, row2):
                    s += x * y
                new_row.append(s)
            mx.append(new_row)
        return Matrix(mx)

    # Part 5
    def transpose(self):
        return Matrix([[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))])

    # Part 6
    def tr(self):
        if self.size()[0] != self.size()[1]:
            raise MatrixSizeError
        s = 0
        for i in range(len(self.matrix)):
            s += self.matrix[i][i]
        return s

    def det(self):
        if self.size()[0] != self.size()[1]:
            raise MatrixSizeError
        if len(self.matrix) == 1:
            return self.matrix[0][0]
        d = self.__small_det(self.matrix)
        if d: return d
        return self.__det(self.matrix)  # as it is recursive

    def __det(self, mx: list):
        d = self.__small_det(mx)
        if d: return d

        s = 0
        cols = len(mx[0])
        for col in range(cols):
            mx_sub = deepcopy(mx)
            mx_sub = mx_sub[1:]  # remove first row
            rows = len(mx_sub)

            for row in range(rows):
                mx_sub[row].pop(col)

            sign = (-1) ** (col % 2)
            sub_det = self.__det(mx_sub)
            s += sign * mx[0][col] * sub_det

        return s

    @staticmethod
    def __small_det(mx: list):
        if len(mx) == 2 and len(mx) == 2:
            return mx[0][0] * mx[1][1] - mx[1][0] * mx[0][1]
        else:
            return None



# from matrix_class import Matrix
# mx1 = Matrix([[2, 1, 4], [0, 1, 1]])
# mx2 = Matrix([[6, 3, -1, 0], [1, 1, 0, 4], [-2, 5, 0, 2]])
# mx1 *= mx2
