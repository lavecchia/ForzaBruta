import array
import math
import numpy

#Library 

def find_distance(x1,y1,z1,x2,y2,z2):
	x=x1-x2
	y=y1-y2
	z=z1-z2
	distance = math.sqrt(x*x+y*y+z*z)
	return(distance)

test=0


R = numpy.zeros(shape=(3,3))


x2 = -3.66829
y2 = 2.41109
z2 =-0.00000

x3 = -1.00841
y3 = 2.44032
z3 = 0.00000

x4 = 0.30691        
y4 = 3.98926        
z4 = 0.00000

newpos= [[0],[0],[0]]

def find_torsion_coordinates(x2, y2, z2, x3, y3, z3,x4, y4, z4, thita):
	if(test==0):
		thita = - thita * 3.14159 / 180
		distance = find_distance(x3,y3,z3,x2,y2,z2)
		l = (x3-x2)/distance
		m = (y3-y2)/distance
		n = (z3-z2)/distance
         	bra = 1-math.cos(thita)
		si = math.sin(thita)
		co = math.cos(thita)
		R[0][0] = l*l*bra+co
		R[1][0] = l*m*bra+n*si
		R[2][0] = l*n*bra-m*si
		R[0][1] = l*m*bra-n*si
		R[1][1] = m*m*bra+co
		R[2][1] = m*n*bra+l*si
  		R[0][2] = l*n*bra+m*si
		R[1][2] = m*n*bra-l*si
		R[2][2] = n*n*bra+co
		x = R[0][0]*(x4-x3)+R[1][0]*(y4-y3)+R[2][0]*(z4-z3)
		y = R[0][1]*(x4-x3)+R[1][1]*(y4-y3)+R[2][1]*(z4-z3)
		z = R[0][2]*(x4-x3)+R[1][2]*(y4-y3)+R[2][2]*(z4-z3)
         	x += x3
		y += y3
		z += z3
	else:
		x = R[0][0]*(x4-x3)+R[1][0]*(y4-y3)+R[2][0]*(z4-z3)
		y = R[0][1]*(x4-x3)+R[1][1]*(y4-y3)+R[2][1]*(z4-z3)
		z = R[0][2]*(x4-x3)+R[1][2]*(y4-y3)+R[2][2]*(z4-z3)
		x += x3
		y += y3
		z += z3
	newpos[0]=x
	newpos[1]=y
	newpos[2]=z
	return newpos

thita = 90

print find_torsion_coordinates(x2, y2, z2, x3, y3, z3,x4, y4, z4, thita)

