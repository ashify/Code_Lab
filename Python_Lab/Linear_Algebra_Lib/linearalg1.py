import math


class Vector:

    def __init__(self, coordinates):
        self.coordinates = tuple(coordinates)
        self.dimensions  = len(self.coordinates)

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
        try:
            return self.scalarMultiply(1/self.getMagnitude())

        except ZeroDivisionError:
            raise Exception('Cannot normalize zero vector')


    def dotProduct(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])
       
    
    def dotProductAngle(self, v, inRadians=False):
        normalized1 = self.normalize()
        normalized2 = v.normalize()
        radians = math.acos(normalized1.dotProduct(normalized2))
        
        if(inRadians):
            return radians

        return math.degrees(radians)


    def isZeroVector(self):
        return self.getMagnitude() < 1e-10 
       

    def isParallelTo(self, v):
        return self.isZeroVector() or v.isZeroVector() or self.dotProductAngle(v,True) == 0 or self.dotProductAngle(v,True) == math.pi


    def isOrthogonalTo(self, v):
        return abs(self.dotProduct(v)) < 1e-10
