import math

class Vector:

    def __init__(self, coordinates):
        self.coordinates = tuple(coordinates)
        self.dimensions  = len(coordinates)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


    def addVector(self, v):
        if(self.dimensions != v.dimensions):
            return 'These vectors are of different dimensions!'
        
        vectorSum = []

        for x,y in zip(self.coordinates, v.coordinates):
            vectorSum.append(x + y)
            
        return Vector(vectorSum)


    def subtractVector(self, v):
        if(self.dimensions != v.dimensions):
            return 'These vectors are of different dimensions!'

        vectorDifference = []

        for x,y in zip(self.coordinates, v.coordinates):
            vectorDifference.append(x - y)

        return Vector(vectorDifference)


    def scalarMultiply(self, v):
        vectorProduct = []

        for x in self.coordinates:
            vectorProduct.append(x*v)

        return Vector(vectorProduct)


    def getMagnitude(self):
        squaredValues = [x**2 for x in self.coordinates]
        return math.sqrt(sum(squaredValues))


    def normalize(self):
        return self.scalarMultiply(1/self.getMagnitude())
