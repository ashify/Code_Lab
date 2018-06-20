from linearalg1 import Vector

# myvector = Vector((8.218,-9.341))
#
# myvector2 = Vector((-1.129,2.111))
#
# vectorSum = myvector.addVector(myvector2)
#
# print(vectorSum)
#
#
# myvector = Vector((7.119,8.215))
#
# myvector2 = Vector((-8.223,0.878))
#
# vectorDifference = myvector.subtractVector(myvector2)
#
# print(vectorDifference)
#
#
# myvector = Vector((1.671,-1.012,-0.318))
#
# vectorProduct = myvector.scalarMultiply(7.41)
#
# print(vectorProduct)

# myvector = Vector((0.221,7.437))

# print(myvector.getMagnitude())


# myvector = Vector((8.813,1.331,6.247))

# print(myvector.getMagnitude())


# myvector = Vector((5.581,-2.136))

# print(myvector.normalize())


# myvector = Vector((1.996,3.108,-4.554))

# print(myvector.normalize())


myvector = Vector((7.887,4.138))

myvector2 = Vector((-8.802,6.776))

print(myvector.dotProduct(myvector2))


myvector = Vector((-5.955,-4.904,-1.874))

myvector2 = Vector((-4.496,-8.755,7.103))

print(myvector.dotProduct(myvector2))


myvector = Vector((3.183,-7.627))

myvector2 = Vector((-2.668,5.319))

print(myvector.dotProductAngle(myvector2, True))


myvector = Vector((7.35,0.221,5.188))

myvector2 = Vector((2.751,8.259,3.985))

print(myvector.dotProductAngle(myvector2))