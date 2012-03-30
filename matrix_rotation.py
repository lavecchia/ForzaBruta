import array
import math
import numpy 
import read_mol2


'''
Generate matrix that contains elements with values 1 and 0 for bonded and unbonded atoms respectivily. 
Matrix element of atom with itself is consider 0.
Input:
    - num_atoms/int: numbers of atoms
    - num_bonds/int: numbers of bonds
    - bonds/list: [[IDatom_orig1, IDatom_target1], [IDatom_orig2, IDatom_target2], ...]
'''
class ConnectivityMatrix:
    def __init__(self, num_atoms, num_bonds, bonds):
        self.num_atoms = num_atoms
        self.num_bonds = num_bonds
        self.bonds = bonds
        pass
    
    #return the connectivity matrix
    def connectivity_matrix(self):
        # generate a empty matrix of natoms x natoms
        cmatrix = numpy.zeros(shape=(self.num_atoms,self.num_atoms))
        # itarative over all bonds
        for ibonds in range(0,self.num_bonds):
            # assing 1 if atoms are bonded. precaution: atomid - 1 = column or row number. ie atom 1 = column/row 0, ...
            cmatrix[self.bonds[ibonds][0] - 1,self.bonds[ibonds][1] -1 ] = 1
        return cmatrix



#Library 

def find_distance(x1,y1,z1,x2,y2,z2):
    x=x1-x2
    y=y1-y2
    z=z1-z2
    distance = math.sqrt(x*x+y*y+z*z)
    return(distance)

test=0


R = numpy.zeros(shape=(3,3))


x2 =-3.66829
y2 = 2.41109
z2 =-0.00000

x3 =-1.00841
y3 = 2.44032
z3 = 0.00000

x4 = 0.30691        
y4 = 3.98926        
z4 = 0.00000

newpos= [[0],[0],[0]]

def find_torsion_coordinates2(x2, y2, z2, x3, y3, z3,x4, y4, z4, thita):
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


coordinate = numpy.matrix(((2.1420,  1.3950, -8.9320),
    (3.6310,  1.4160, -8.5370),
    (4.2030, -0.0120, -8.6120),
    (5.6910,  0.0090, -8.2180),
    (1.6040,  0.7600, -8.2600),
    (1.7450,  2.3880, -8.8800),
    (2.0430,  1.0240, -9.9300),
    (4.1690,  2.0510, -9.2100),
    (3.7310,  1.7880, -7.5390),
    (3.6650, -0.6470, -7.9400),
    (4.1040, -0.3840, -9.6100),
    (5.7930,  0.3880, -7.2010),
    (6.2400,  0.6560, -8.9030),
    (6.2630, -1.4180, -8.2930),
    (6.1620, -1.7970, -9.3090),
    (5.7150, -2.0650, -7.6080),
    (7.3160, -1.4030, -8.0130)))


def find_torsion_coordinates(atom1, atom2, coordinate, thita):
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
        rotation = numpy.matrix(R)
                
        newcoordinate = ((coordinate - (x3,y3,z3)) * rotation) + (x3,y3,z3)


    print newcoordinate
    

thita = 90

print find_torsion_coordinates(x2, y2, z2, x3, y3, z3,coordinate, thita)

