import read_mol2
import search_rotatable
import matrix_rotation

data = open("pentane.mol2", 'r')

prueba = read_mol2.ReadMol2(data)

#print str(prueba.atoms[1].atom_type)

#for i in range(0,prueba.num_atoms):
#	print prueba.atoms[i].atom_type
	
#print prueba.atoms[2]
#print prueba.get_atom(2).atom_type


#print prueba.get_bonded_atoms(14)[0].atom_id
#print prueba.get_bonded_atoms(14)[1].atom_id
#print prueba.get_bonded_atoms(14)[2].atom_id
#print prueba.get_bonded_atoms(14)[3].atom_id



#print prueba.get_bonded_atoms(17)[0].atom_id
#print "longitud:" + str(len(prueba.get_bonded_atoms(14)))
#print prueba.bonds[1]

print search_rotatable.SearchRotatable(prueba)

bonds = []

for ind in range(0,prueba.num_bonds):
    bonds.append([prueba.bonds[ind].origin_atom_id,prueba.bonds[ind].target_atom_id])

cmatrix = matrix_rotation.ConnectivityMatrix(prueba.num_atoms,prueba.num_bonds, bonds)


print cmatrix.connectivity_matrix()
