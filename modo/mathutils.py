#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

import lx
from lxu import vector
import math
import sys
from collections import Iterable

QX = 0
QY = 1
QZ = 2
QW = 3

MIN_PRECISION = sys.float_info.min


class Matrix3(object):
    """Matrix3 class """

    def __init__(self, other=None):
        """Initializes a Matrix object

        :param other: Copies from other Matrix3 (optional)
        :type other: Matrix3
        returns: Matrix3
        """

        self.m = []
        self.size = 3

        self.setIdentity()
        if other:
            # TODO: look into removing redundant conversion
            if isinstance(other, lx.object.Unknown):
                inmat = lx.object.Matrix(other)
                self.set(inmat.Get3())
            if isinstance(other, lx.object.Matrix):
                self.set(other.Get3())
            if isinstance(other, Matrix4):
                for row in range(3):
                    for column in range(3):
                        self.m[row][column] = other[row][column]
            else:
                self.set(other)

    @staticmethod
    def _getIdentity(size=None):

        mat = []
        size = 3 if size is None else size

        for row in range(size):
            r = [0.0 for i in range(size)]
            r[row] = 1.0
            mat.append(r)
        return mat

    def __mul__(self, other):
        """
        Multiply with other matrix
        
        :param other: Matrix to multiply with
        :type other: Matrix3
        
        """
        matrixTmp, matrixResult = self.__class__(), self.__class__()

        for i in range(self.size):
            for j in range(self.size):
                matrixTmp.m[i][j] = 0.0

        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    matrixTmp.m[i][j] += self.m[i][k] * other.m[k][j]

        for i in range(self.size):
            for j in range(self.size):
                matrixResult.m[i][j] = matrixTmp.m[i][j]

        return matrixResult

    def __repr__(self):
        """

        :returns basestring: String representation of the Matrix
        """
        return "%s(%s)" % (self.__class__.__name__, str(self.m))

    def __len__(self):
        """

        :returns int: The size of the Matrix
        """
        return len(self.m)

    def __getitem__(self, index):
        """
        :param index: Row-index
        :type index: Int
        :returns list: A row from the Matrix
        """
        return self.m[index]

    def __setitem__(self, index, value):
        """
        :param index: Row-index
        :type index: Int
        """
        for i in range(len(value)):
            self.m[index][i] = value[i]
        # self.m[index] = value

    def __eq__(self, other):
        """Test for equality against other Matrix

        :param other:
        :return:
        """
        if isinstance(other, (list, tuple)):
            other = self.__class__(other)
        if isinstance(other, (Matrix3, Matrix4)):

            equal = False

            if self.size != other.size:
                return equal

            for column in range(self.size):
                for i, j in zip(self.m[column], other.m[column]):
                    if abs(i - j) > 0.0000000001:
                        return False
            return True
        else:
            raise TypeError

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    @staticmethod
    def _MatrixToEuler(m, order='zxy'):

        axes = {'x':0, 'y':1, 'z':2}
        i, j, k = (axes[char] for char in order.lower())

        eAngles = [0] * 3
        s = math.sqrt(m[i][i] * m[i][i] + m[j][i] * m[j][i])

        if s > 16 * sys.float_info.epsilon:
            eAngles[0] = math.atan2(m[k][j], m[k][k])
            eAngles[1] = math.atan2(-m[k][i], s)
            eAngles[2] = math.atan2(m[j][i], m[i][i])
        else:
            eAngles[0] = math.atan2(-m[j][k], m[j][j])
            eAngles[1] = math.atan2(-m[k][i], s)
            eAngles[2] = 0.0

        # parity is even if the inner axis X is followed by the middle axis Y,
        # or Y is followed by Z, or Z is followed by X

        if (i == 0 and j != 1) or (i == 1 and j != 2) or (i == 2 and j != 0):

            # parity is odd - whatever that means
            eAngles[0] = -eAngles[0]
            eAngles[1] = -eAngles[1]
            eAngles[2] = -eAngles[2]

        if (i, j, k) == (1, 2, 0):
            eAngles[0], eAngles[1], eAngles[2] = eAngles[1], eAngles[2], eAngles[0]

        elif (i, j, k) == (2, 0, 1):
            eAngles[0], eAngles[1], eAngles[2] = eAngles[2], eAngles[0], eAngles[1]

        # if rotating:
        #     eAngles[2], eAngles[1] = eAngles[1], eAngles[2]

        return eAngles[i], eAngles[j], eAngles[k]

    def set(self, other, transpose=True):
        """Copy values from other Matrix

        :param Matrix other: Source Matrix
        """
        if isinstance(other, Matrix3):
            self.m = [list(row[:]) for row in other.m]
        elif isinstance(other, (tuple, list)):
            # Input is a 3x3 matrix
            if len(other[0]) == 3:
                self.m = [list(row[:]) for row in other]
            # Input is a 4x4 matrix
            else:
                self.m = [list(row[:]) for row in other]

        # if transpose:
        #     self.m = self.transposed().m

    def copy(self):
        """
        :return: A copy of this Matrix
        """
        return self.__class__(self.m)

    def setIdentity(self):
        """Set this matrix to it's identity """

        self.m = Matrix3._getIdentity(self.size)
        # self.m = Matrix3._getIdentity()

    def transpose(self):
        """This function transposes a matrix, by flipping it across it's main
        diagonal."""
        # self.m = Matrix3(self).transposed().m
        self.m = self.__class__(self).transposed().m

    def transposed(self):
        """This function transposes a matrix, by flipping it across it's main
        diagonal. It returns a new transposed matrix. """

        # out_mat = Matrix3(self)
        out_mat = self.__class__(self)

        for i in range(self.size):
            for j in range(self.size):
                out_mat.m[i][j] = self.m[j][i]

        return out_mat

    def asEuler(self, degrees=False, order='zxy'):
        """Returns euler values from the Matrix

        :param bool degrees: If True, the values are returned as degrees, otherwise as radians
        :param basestring order: The rotation order to return values for.
        :return list: Euler values
        """
        euler = Matrix3._MatrixToEuler(self, order)
        if degrees:
            return [math.degrees(angle) for angle in euler]
        return euler

    def inverted(self):
        """

        :returns Matrix: An inverted copy of this Matrix
        """
        tmp = Matrix4(self)
        tmp.invert()
        return Matrix3(tmp)

    def invert(self):
        """Inverts this Matrix in place
        """
        self.m = self.inverted().m


class Matrix4(Matrix3):
    """Matrix class """

    def __init__(self, other=None, position=None):
        """Initializes a Matrix object

        :param other: Copies from other Matrix4 (optional)
        :type other: Matrix4
        :param position: Translation value to set (optional)
        :type position: iterable
        returns: Matrix4
        """

        self.m = []
        self.size = 4

        self.setIdentity()
        if other:
            if isinstance(other, lx.object.Unknown):
                inmat = lx.object.Matrix(other)
                self.set(inmat.Get4())
            if isinstance(other, Matrix4):
                self.set(other)
            elif isinstance(other, Matrix3):
                for row_num, row in enumerate(other):
                    for column in range(len(row)):
                        self.m[row_num][column] = other[row_num][column]
            elif isinstance(other, lx.object.Matrix):
                self.set(other.Get4())

            else:
                self.set(other)

        if position:
            for i, v in enumerate(position):
                self.m[3][i] = v

    def set(self, other):
        if isinstance(other, Matrix4):
            self.m = [list(row[:]) for row in other.m]
        elif isinstance(other, Iterable):
            # Input is a 3x3 matrix
            if len(other[0]) == 3:
                self.m = [list(row[:])+[0] for row in other]
                self.m.append([0, 0, 0, 1])
            # Input is a 4x4 matrix
            else:
                self.m = [list(row[:]) for row in other]

    def asRotateMatrix(self):
        """Removes the translation part of this Matrix """
        retM = Matrix4()

        for i in range(3):
            for j in range(3):
                retM.m[i][j] = self.m[i][j]

        return retM

    @property
    def position(self):
        """
        :getter: Returns the translation part of this matrix
        :rtype: tuple

        :setter: Sets the translation part of this matrix
        :param position: Position
        :type position: iterable
        """
        return (self.m[3][0], self.m[3][1], self.m[3][2])

    @position.setter
    def position(self, position):
        for i, v in enumerate(position):
            self.m[3][i] = v

    def inverted(self):
        output = Matrix4._getIdentity(self.size)

        a0 = self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]
        a1 = self.m[0][0] * self.m[1][2] - self.m[0][2] * self.m[1][0]
        a2 = self.m[0][0] * self.m[1][3] - self.m[0][3] * self.m[1][0]
        a3 = self.m[0][1] * self.m[1][2] - self.m[0][2] * self.m[1][1]
        a4 = self.m[0][1] * self.m[1][3] - self.m[0][3] * self.m[1][1]
        a5 = self.m[0][2] * self.m[1][3] - self.m[0][3] * self.m[1][2]
        b0 = self.m[2][0] * self.m[3][1] - self.m[2][1] * self.m[3][0]
        b1 = self.m[2][0] * self.m[3][2] - self.m[2][2] * self.m[3][0]
        b2 = self.m[2][0] * self.m[3][3] - self.m[2][3] * self.m[3][0]
        b3 = self.m[2][1] * self.m[3][2] - self.m[2][2] * self.m[3][1]
        b4 = self.m[2][1] * self.m[3][3] - self.m[2][3] * self.m[3][1]
        b5 = self.m[2][2] * self.m[3][3] - self.m[2][3] * self.m[3][2]

        det = a0 * b5 - a1 * b4 + a2 * b3 + a3 * b2 - a4 * b1 + a5 * b0

        if abs (det) <= 0.00001:
            return self.m

        output[0][0] = 0.0 + self.m[1][1] * b5 - self.m[1][2] * b4 + self.m[1][3] * b3
        output[1][0] = 0.0 - self.m[1][0] * b5 + self.m[1][2] * b2 - self.m[1][3] * b1
        output[2][0] = 0.0 + self.m[1][0] * b4 - self.m[1][1] * b2 + self.m[1][3] * b0
        output[3][0] = 0.0 - self.m[1][0] * b3 + self.m[1][1] * b1 - self.m[1][2] * b0
        output[0][1] = 0.0 - self.m[0][1] * b5 + self.m[0][2] * b4 - self.m[0][3] * b3
        output[1][1] = 0.0 + self.m[0][0] * b5 - self.m[0][2] * b2 + self.m[0][3] * b1
        output[2][1] = 0.0 - self.m[0][0] * b4 + self.m[0][1] * b2 - self.m[0][3] * b0
        output[3][1] = 0.0 + self.m[0][0] * b3 - self.m[0][1] * b1 + self.m[0][2] * b0
        output[0][2] = 0.0 + self.m[3][1] * a5 - self.m[3][2] * a4 + self.m[3][3] * a3
        output[1][2] = 0.0 - self.m[3][0] * a5 + self.m[3][2] * a2 - self.m[3][3] * a1
        output[2][2] = 0.0 + self.m[3][0] * a4 - self.m[3][1] * a2 + self.m[3][3] * a0
        output[3][2] = 0.0 - self.m[3][0] * a3 + self.m[3][1] * a1 - self.m[3][2] * a0
        output[0][3] = 0.0 - self.m[2][1] * a5 + self.m[2][2] * a4 - self.m[2][3] * a3
        output[1][3] = 0.0 + self.m[2][0] * a5 - self.m[2][2] * a2 + self.m[2][3] * a1
        output[2][3] = 0.0 - self.m[2][0] * a4 + self.m[2][1] * a2 - self.m[2][3] * a0
        output[3][3] = 0.0 + self.m[2][0] * a3 - self.m[2][1] * a1 + self.m[2][2] * a0

        inv_det = 1.0 / det

        for i in range (4):
            for j in range (4):
                output[i][j] = output[i][j] * inv_det

        return Matrix4(output)

    def determinant(self):
        m = [list(row[:]) for row in self.m]
        a0 = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        a1 = m[0][0] * m[1][2] - m[0][2] * m[1][0]
        a2 = m[0][0] * m[1][3] - m[0][3] * m[1][0]
        a3 = m[0][1] * m[1][2] - m[0][2] * m[1][1]
        a4 = m[0][1] * m[1][3] - m[0][3] * m[1][1]
        a5 = m[0][2] * m[1][3] - m[0][3] * m[1][2]
        b0 = m[2][0] * m[3][1] - m[2][1] * m[3][0]
        b1 = m[2][0] * m[3][2] - m[2][2] * m[3][0]
        b2 = m[2][0] * m[3][3] - m[2][3] * m[3][0]
        b3 = m[2][1] * m[3][2] - m[2][2] * m[3][1]
        b4 = m[2][1] * m[3][3] - m[2][3] * m[3][1]
        b5 = m[2][2] * m[3][3] - m[2][3] * m[3][2]

        return a0 * b5 - a1 * b4 + a2 * b3 + a3 * b2 - a4 * b1 + a5 * b0

    def asEuler(self, degrees=False, order='zxy'):
        euler = Matrix4._MatrixToEuler(self.transposed(), order)
        if degrees:
            return [math.degrees(angle) for angle in euler]
        return euler

    @staticmethod
    def _matrix_vectorMultiply (matrix, vector):
        """

        :param matrix:
        :param vector:
        :param result:
        :return:
        """
        # void util_value::matrix_vectorMultiply (LXtMatrix4 matrix, LXtVector vector, LXtVector result)
        # This function multiplies a vector by a matrix, resulting in a new
        # vector. This is useful for applying a transform to a position in 3D
        # space.

        result = Vector3()
        result[0] = vector[0] * matrix[0][0] + vector[1] * matrix[1][0] + vector[2] * matrix[2][0] + matrix[3][0]
        result[1] = vector[0] * matrix[0][1] + vector[1] * matrix[1][1] + vector[2] * matrix[2][1] + matrix[3][1]
        result[2] = vector[0] * matrix[0][2] + vector[1] * matrix[1][2] + vector[2] * matrix[2][2] + matrix[3][2]
        return result

    # @property
    def scale(self):
        return Vector3( [Vector3(self.m[i]).length() for i in range(3)] )

    @staticmethod
    def _rotOrderToList(text='zxy'):
        '''
        takes a string in form of 'xyz' and returns a list in form of [0,1,2]
        '''
        axes = {'x':0, 'y':1, 'z':2}
        return [axes[char] for char in text.lower()]
        
    @staticmethod
    def fromEuler(angles, order='zxy'):

        # This function converts a euler rotation vector into a rotation matrix.
        # The orders argument specifies the order the rotations are applied to
        # to the matrix.

        # Convert order string to list
        orders = Matrix4._rotOrderToList(order)

        matrix = Matrix4()

        for i in range(3):
            matrix_temp = Matrix4._matrix_calcRotation(angles[orders[i]], orders[i])
            matrix *= Matrix3(matrix_temp)

        return matrix

    # void util_value::matrix_calcRotation (double angle, int axis, LXtMatrix4 matrix)
    @staticmethod
    def _matrix_calcRotation (angle, axis):

        # This function calculates a rotation matrix, based on a specific angle
        # and axis. The resulting matrix will store the rotation amount around
        # the specified axis.

        axis0 = [1, 2, 0]
        axis1 = [2, 0, 1]

        # matrix_identity(matrix);
        matrix = Matrix4._getIdentity(4)

        a = axis0[axis]
        b = axis1[axis]

        s = math.sin(angle)

        matrix[b][a] = -s
        matrix[a][b] = s
        matrix[a][a] = math.cos(angle)
        matrix[b][b] = math.cos(angle)

        return matrix


class Vector3(object):
    """Vector3 class
    """

    def __init__(self, *a):
        """

        :param float a: Three float values
        :return Vector3: The initialized Vector3 object
        """

        self.values = [0, 0, 0]

        n = len(a)
        # Constructing from three literal numbers
        if n >= 3:
            for i in range(3):
                self.values[i] = a[i]

        # Constructing from single argument
        elif n == 1:
            # If vector, copy values
            if isinstance(a[0], Vector3):
                self.values = a[0].values[:]
            # Single argument is an iterable (i.e. list or tuple)
            elif isinstance(a[0], Iterable):
                _list = a[0]
                self.values = [_list[i] for i in range(3)]
            # Copy the argument value to all slots
            else:
                self.values = [a[0] for i in range(3)]

    @property
    def x(self):
        """Quick access to the x component of the vector"""
        return self.values[0]

    # Prevent from setting to int?
    @x.setter
    def x(self, value):
        self.values[0] = value

    @property
    def y(self):
        """Quick access to the y component of the vector"""
        return self.values[1]

    @y.setter
    def y(self, value):
        self.values[1] = value

    @property
    def z(self):
        """Quick access to the z component of the vector"""
        return self.values[2]

    @z.setter
    def z(self, value):
        self.values[2] = value

    def __repr__(self):
        "Returns a string representation of this vector"
        return "%s(%f, %f, %f)" % (self.__class__.__name__, self.values[0], self.values[1], self.values[2])

    def __add__(self, other):
        """Vector Addition"""
        if isinstance(other, (list, tuple)):
            return Vector3(list(vector.add(self.values, other)))
        return Vector3(list(vector.add(self.values, other.values)))

    def __sub__(self, other):
        """Vector Subtraction"""
        if isinstance(other, (list, tuple)):
            return Vector3(list(vector.sub(self.values, other)))
        return Vector3(list(vector.sub(self.values, other.values)))

    def __mul__(self, other):
        """Vector multiplication

        :param other: Can be another Vector3, a Matrix4 or a float value.
        
        When other is a Vector3 the result is a component-wise multiplication
        """

        # Scale this vector by scalar value
        if isinstance(other, int) or isinstance(other, float):
            return Vector3(vector.scale(self.values, other))

        # component-wise multiplication 
        elif isinstance(other, Vector3):
            return Vector3( [a*b for a,b in zip(self.values, other.values)] )

        elif isinstance(other, Matrix4):
            raise NotImplementedError("Please use Vector3.mulByMatrixAsPoint instead")
        return self

    def __truediv__(self, other):
        """Vector division"""
        if isinstance(other, (float, int)):
            return Vector3([value/other for value in self.values])
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.values))

    def dot(self, other):
        if isinstance(other, Vector3):
            return vector.dot(self.values, other.values)
        return vector.dot(self.values, other)

    # @property
    def length(self):
        """Returns the length of this vector"""
        return vector.length(self.values)

    def setLength(self, value):
        """Sets the length of this vector"""
        tmp = Vector3(self.values)
        tmp.normalize()
        tmp *= value
        self.values = tmp.values

    def __len__(self):
        """Returns the number of vector components"""
        return len(self.values)

    def copy(self):
        return Vector3(self.values[:])

    def normal(self):
        """Returns a normalized copy of this vector"""
        return Vector3(vector.normalize(self.values))

    def normalize(self):
        """Normalizes this vector in place"""
        self.values = list(vector.normalize(self.values))

    def cross(self, other):
        """Returns a new vector with the result of crossing this vector with another"""
        return Vector3(vector.cross(self.values, other.values))

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def angle(self, other):
        """Returns the angle between this and another vector"""
        return math.acos(self.normal().dot(other.normal()))

    def equals(self, other, tolerance=None):
        """Returns if this vector is equivalent to another vector"""

        # If is sequence convert to vector
        if isinstance(other, (list, tuple)):
            other = Vector3(other)

        tolerance = 0.0000000001 if not tolerance else tolerance
        return (self - other).length() <= tolerance

    def __eq__(self, other):
        """Returns if this vector is equivalent to another vector"""
        return self.equals(other)

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def rotate(self, other):
        # by matrix, quaternion, euler etc.
        raise NotImplementedError

    def rotateByQuat(self, other):
        """Rotate this vector by a quaternion"""
        matrix = Matrix4(position=self.values)
        matrix = matrix * other.toMatrix4()
        for i in range(3):
            self.values[i] = matrix[3][i]

    def rotateByAxisAngle(self, axis, angle):
        """Rotates this vector by a given axis and angle

        :param Vector3 axis: This axis to rotate about
        :param float angle: The angle in radians to rotate by
        """
        quat = Quaternion()
        quat.setAxisAngle(axis, angle)
        result = Matrix4(position=self.values) * quat.toMatrix4()
        self.values = list(result.position)

    def distanceBetweenPoints(self, other):
        """Returns the distance between this and another point"""
        tmp = Vector3(self) - Vector3(other)
        return tmp.length()

    def mulByMatrixAsPoint(self, other):
        """Transform this point's position by a Matrix4 in place.

        :param Matrix4 other: Other Matrix
        """
        # Multiply by a matrix
        if isinstance(other, Matrix4):
            result = Matrix4._matrix_vectorMultiply(other, self)
            self.values = Vector3(result).values
            
    def lerp(self, other, t):
        """Perform linear blending between this and other Vector3
        
        :param Vector3 other: Other vector
        :param float t: Parameter between 0.0 and 1.0        
        """        
        return self*(1-t) + other*t        
        

class Quaternion(object):
    """Minimal quaternion class"""

    def __init__(self, values=None):
        if not values:
            self.values = [0, 0, 0, 1.0]

        else:
            if not len(values) == 4:
                raise ValueError("Need to provide four float values")
            self.values = values

    def __repr__(self):
        """Returns a string representation of this Quaternion"""
        return "%s(%f, %f, %f, %f)" % (self.__class__.__name__, self.values[0], self.values[1], self.values[2], self.values[3])

    @property
    def x(self):
        """Quick access to the x component of the quaternion"""
        return self.values[0]

    @x.setter
    def x(self, value):
        self.values[0] = value

    @property
    def y(self):
        """Quick access to the y component of the quaternion"""
        return self.values[1]

    @y.setter
    def y(self, value):
        self.values[1] = value

    @property
    def z(self):
        """Quick access to the z component of the quaternion"""
        return self.values[2]

    @z.setter
    def z(self, value):
        self.values[2] = value

    @property
    def w(self):
        """Quick access to the w component of the quaternion"""
        return self.values[3]

    @w.setter
    def w(self, value):
        self.values[3] = value

    def __setitem__(self, index, value):
        self.values[index] = value

    def __getitem__(self, index):
        return self.values[index]

    @staticmethod
    def __dTolerance(d):

        # This function returns a tolerance value for any given input. The value
        # returned will be a positive number which is much smaller in magnitude
        # than the input, representing the minimum change required to make this
        # value different.

        if d < 0.0:
            d /= -3.36e6
        else:
            d /=  3.36e6

        if d > MIN_PRECISION:
            return d
        else:
            return MIN_PRECISION

    @staticmethod
    def _quaternion_length(q_):
        """This function calculates the length of the quaternion.

        :param Quaternion q:
        :returns float:
        """
        return math.sqrt((q_[QX] * q_[QX]) + (q_[QY] * q_[QY]) + (q_[QZ] * q_[QZ]) + (q_[QW] * q_[QW]))

    @staticmethod
    def _quaternion_identity(q):
        return [0.0, 0.0, 0.0, 1.0]

    @staticmethod
    def _quaternion_normalize(q):
        """This function normalizes a quaternion, setting the length of the quaternion to 1.0.

        :param Quaternion q:
        :return:
        """

        mag = 0.0

        mag = Quaternion._quaternion_length(q)

        if mag > 0.0:
            q[QX] /= mag
            q[QY] /= mag
            q[QZ] /= mag
            q[QW] /= mag
        else:
            q = Quaternion._quaternion_identity(q)

        return q

    def copy(self):
        """Returns a copy of this quaternion object"""
        return Quaternion(self.values[:])

    def setAxisAngle(self, axis, angle):
        """This function takes an axis and an angle, and calculates a quaternion that encodes that rotation.

        :param float angle: Angle in radians
        :param Vector3 axis: Axis
        """

        q = [0, 0, 0, 1.0]
        # s = 0.0

        if isinstance(axis, (list, tuple)):
            axis = Vector3(axis)

        axis.normalize()

        s = math.sin(angle * 0.5)

        q[QX] = s * axis[0]
        q[QY] = s * axis[1]
        q[QZ] = s * axis[2]
        q[QW] = math.cos(angle * 0.5)

        self.values = q

    def getAxisAngle(self):
        """Returns the axis and angle of this quaternion

        :returns tuple: Axis [tuple] and angle [float]
        """

        q_temp = self.values[:]
        q = self.values[:]

        omega, s = 0.0, 0.0

        q_temp = self.values
        q_temp = Quaternion._quaternion_normalize(q_temp)

        axis = [0.0, 0.0, 0.0]

        axis[0] = q[0]
        axis[1] = q[1]
        axis[2] = q[2]

        omega = math.acos(q_temp[QW])

        angle = 2.0 * omega

        s = math.sin(omega)

        if s != 0.0:
            axis[0] /= s
            axis[1] /= s
            axis[2] /= s

        return axis, angle

    def normalize(self):
        """Normalizes the quaternion in place"""
        self.values = Quaternion._quaternion_normalize(self.values)

    def length(self):
        """Returns the length of this quaternion"""
        return Quaternion._quaternion_length(self.values)

    def toMatrix3(self):
        """This function converts a quaternion into a Matrix3, containing the same rotation.

        :return Matrix3: Result
        """

        input = self.values
        output = Matrix3._getIdentity(size=3)

        norm, s = 0.0, 0.0
        xx, yy, zz = 0.0, 0.0, 0.0
        xy, xz, yz = 0.0, 0.0, 0.0
        wx, wy, wz = 0.0, 0.0, 0.0

        norm = input[QX] * input[QX] + input[QY] * input[QY] + input[QZ] * input[QZ] + input[QW] * input[QW]
        # s = (norm > __dTolerance (norm)) ? 2.0 / norm : 0
        s = 2.0 if (norm > Quaternion.__dTolerance(norm)) else 0

        xx = input[QX] * input[QX] * s
        yy = input[QY] * input[QY] * s
        zz = input[QZ] * input[QZ] * s
        xy = input[QX] * input[QY] * s
        xz = input[QX] * input[QZ] * s
        yz = input[QY] * input[QZ] * s
        wx = input[QW] * input[QX] * s
        wy = input[QW] * input[QY] * s
        wz = input[QW] * input[QZ] * s

        output[0][0] = 1.0 - (yy + zz)
        output[0][1] = xy + wz
        output[0][2] = xz - wy

        output[1][0] = xy - wz
        output[1][1] = 1.0 - (xx + zz)
        output[1][2] = yz + wx

        output[2][0] = xz + wy
        output[2][1] = yz - wx
        output[2][2] = 1.0 - (xx + yy)

        return Matrix3(output)

    def toMatrix4(self):
        """
        :returns Matrix4: This quaternion as Matrix4, containing the same rotation
        """
        matrix = self.toMatrix3()
        matrix.transpose()
        return Matrix4(matrix)

    def fromMatrix3(self, input):
        """ This function converts a matrix into a quaternion, containing the same rotation.

        :param Matrix3 input:
        :param Quaternion output:
        """

        output = Quaternion()

        nxt = [1, 2, 0]
        i, j, k = 0, 0, 0
        tr, s = 0.0, 0.0

        tr = input[QX][QX] + input[QY][QY] + input[QZ][QZ] + 1.0

        if tr > 0.0:
            s = math.sqrt(tr)

            output[QW] = s * 0.5

            s = 0.5 / s

            output[QX] = (input[QZ][QY] - input[QY][QZ]) * s
            output[QY] = (input[QX][QZ] - input[QZ][QX]) * s
            output[QZ] = (input[QY][QX] - input[QX][QY]) * s
        else:
            i = QX

            if input[QY][QY] > input[QX][QX]:
                i = QY

            if input[QZ][QZ] > input[i][i]:
                i = QZ

            j = nxt[i]
            k = nxt[j]

            s = math.sqrt((input[i][i] - (input[j][j] + input[k][k])) + 1.0)

            output[i] = s * 0.5

            if s > 0:
                s = 0.5 / s

            output[QW] = (input[k][j] - input[j][k]) * s
            output[j]  = (input[j][i] + input[i][j]) * s
            output[k]  = (input[k][i] + input[i][k]) * s

        self.values = output

    def fromMatrix4(self, input):
        """ This function converts a matrix into a quaternion, containing the same rotation.

        :param Matrix4 input:
        """
        matrix = Matrix3(input)
        matrix.transpose()

        quat = Quaternion()
        quat.fromMatrix3(matrix)
        self.values = quat.values


