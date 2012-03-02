class SearchRotatable:
    def __init__(self, data):
        natoms = data.num_atoms
        nbonds = data.num_bonds
        print "numero de atomos:" + str(natoms)
        print "numero de enlaces:" + str(nbonds)
        types = []	
        spectypes = []
        m_bonds = []
        ring = {}
        ringbonds = []
        neighb=()
        #create a list containing atom number as a key and type as a value
        for i in range(0,natoms):
            types.append(data.atoms[i].atom_type)
        #       for i in range(0,nbonds):
        #          neighb.append(   

        # before we start looking for non-rotatable bonds we determine if some atoms belong to some more complicated atom types	
        for ind in range(0,len(types)):
            count = 0
            noscount = 0
            # planar amine
            if types[ind] == "N.pl3" or types[ind] == "N.2":
                # there have to be exactly 2 hydrogens connected to it 
                for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
                    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "H":
                        count += 1 
                    if count==2:
    			        spectypes.append('planar_nh2')
            # methyl and as a special case methyl connected to N,O or S.           
            elif types[ind] == "C.3":
                # there have to be exactly 3 hydrogens connected to it 
    			for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "H":
    			        count += 1
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "N." or data.get_bonded_atoms(ind+1)[ibon].atom_type == "O." or data.get_bonded_atoms(ind+1)[ibon].atom_type == "S.":
    			        noscount += 1
    			print "count" + str(count)
    			if count == 3:
    			    if noscount == 1:
    			        spectypes.append('nos_methyl')
    			    else:
    			        spectypes.append('methyl')
            # amidine
            elif types[ind] == "C.2" or types[ind] == "C.cat":
    			for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "N.pl3" or data.get_bonded_atoms(ind+1)[ibon].atom_type == "N.2":
    			        count += 1
    			if count == 2:
    			    spectypes.append('amidine')
            # sulfonic acid
            elif types[ind] == "S.3":
                for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "O.co2":
    			        count += 1
                if count == 3:
                    spectypes.append('sulfonate')
            # nitro,nitroso
            elif types[ind] == "N.":
                for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "O.2":
    			        count += 1
                if count >= 1:
                    spectypes.append('nitro')
            # carboxylic acid
            elif types[ind] == "C.2" or types[ind] == "C.cat":
                for ibon in range(0,len(data.get_bonded_atoms(ind+1))):
    			    if data.get_bonded_atoms(ind+1)[ibon].atom_type == "O.co2":
    			        count += 1
                if count == 2:
                    spectypes.append('carboxy')
            # other
            else:
                spectypes.append(None)
        print types
        print spectypes

        #chequeado hasta aca
        
        
        # initialize edges,     
        edge = {}
        
        for ind in range(0,nbonds):
            
            edge[ind] = [data.bonds[ind].origin_atom_id,data.bonds[ind].target_atom_id] 
        
        
        
        vertex = {}   
        for ind in range(0,len(types)):  
            # initialize vertices; use the number of connectivities (neighbors) as the value.
            vertex[ind+1] = len(data.get_bonded_atoms(ind+1))
        
        nv = len(vertex)            
        ne = len(edge)	    

        print edge
        print vertex
        print "Renewed vertices: "+ str(nv) + " edges : " + str(ne) + " \n"
        vertexcp = vertex.copy()
        edgecp = edge.copy()
  
        oneneighbor = 1
        while oneneighbor > 0:
            vertexcp = vertex.copy()
            edgecp = edge.copy()
            #       delete appendages to the rings. Update %vertex and %edge hashes
            for kvertex, vvertex in vertexcp.iteritems():
                if vvertex == 1:
                    print "se elimino vertex" + str(kvertex)
                    vertex.pop(kvertex)
                    for kedge, vedge in edgecp.iteritems():
                        k1 = vedge[0]
                        k2 = vedge[1]
                        if k1 == kvertex or k2 == kvertex:
                            print "se elimino edge" + str(kedge)
                            edge.pop(kedge)
                            if k1 == kvertex:
                                vertex[k2] -= 1
                            if k2 == kvertex:
                                vertex[k1] -= 1
                                
            oneneighbor = 0
            
            for kvertex, vvertex in vertex.iteritems():
                if vvertex == 1:
                    oneneighbor += 1
                 
        while len(vertex) > 0:
            label={}
            #       reduce the graph further by collapsing other vertices
            #       sort the vertex hash by increasing number of neighbors; pick just one, first vertex
            #vertex.sort() OJO!!!
            for kvertex, vvertex in vertex.iteritems():
                specedge = {}
                for kedge, vedge in edge.iteritems():
                    if vedge[0] == vvertex and vedge[1] != vvertex:
                        specedge[kvertex] = ['F', vedge]
                    if vedge[1] == vvertex and vedge[0] != vvertex:
                        specedge[kvertex] = ['L', vedge]
                    if vedge[1] == vvertex and vedge[0] != vvertex:
                        specedge[kvertex] = ['B', vedge]

            #	pick a number for a label; since we don't want it to accidentally repeat the existing labels, we choose
            #       max of existing labels
            maxlabel = -1
            for kedge, vedge in edge.iteritems():
                if kedge > maxlabel:
                    maxlabel = kedge
              
            #	join the two edges pairwise
            newedg = []
            for kspecedge, vspecedge in specedge.iteritems():
                edge1 = vspecedge
                if edge1[0] == 'B':
                    continue
                for kspecedge2, vspecedge2 in specedge.iteritems():
                    edge2 = vspecedge2
                    if edge2[0] == 'B':
                        continue #OJO!!!! que puede saltar al otro
                    while kspecedge < kspecedge2:
                        tmp1 = edge1[1]
                        tmp2 = edge2[1]
                        if edge1[0] == 'F':
                            tmp1 = tmp1.reverse()
                        if edge2[0] == 'L':
                            tmp2 = tmp2.reverse()
                        # concatenate the two arrays together
                        tmp1.append(tmp2[1])
                        newedg.append(tmp1)

            for knewedge, vnewedg in newedg:
                maxlabel += 1
                for ind in range(0,len(newedg[kspecedge])):
                    edge[maxlabel].add(newedg[kspecedge][ind])
            edgecp = edge.copy()
            for kedge, vedge in edgecp.iteritems():
                if vedge[0] == vedge[-1]:
                    ii = len(vedge)-1
                else:
                    ii = len(vedge)
                # remove edges which have repetitive elements along the path
                for i in range(0,ii):
                    for j in range(0,i-1):
                        if vedge[j] == vedge[i]:
                            edge.pop(kedge)
                            continue
                if vedge[0] == kvertex or vedge[-1] == kvertex:
                    if vedge[0] == vedge[-1]:
                        ring.add(vedge)
                    edge.pop(kedge)
            #	remove vertex
            vertex.pop(kvertex)
            #       recalculate connectivities
            #       zero out connectivities first
            for kvertex,vvertex in vertex.iteritems():
                vertex[kvertex] = 0
                for kedge, vedge in edge.iteritems():
                    if vedge[0] == kvertex or vedge[-1]== kvertex:
                        vertex[kvertex] += 1
                        
	    for iring in range(0,len(ring)):
	        for iring2 in range(0,len(ring)-1):
	            ringbonds.append(ring[iring][iring2,iring2+1])
	            
	    print "ringbonds " + str(ringbonds)
'''
        keeplist = {}
        for ibonds in range(0,nbonds):
            k1 = data.bonds[ibonds].origin_atom_id
            k2 = data.bonds[ibonds].target_atom_id
            #       check for bonds which are inside the rings
            for iringbonds in range(0,len(ringbonds)):
                if (k1 == ringbonds[iringbonds][0] and k2 == ringbonds[iringbonds][1]) or (k1 == ringbonds[iringbonds][1] and k2 == ringbonds[iringbonds][0]):
                    continue

        #       check for bonds which are connected on one end only
        k1num == len(data.get_bonded_atoms[k1])
        k2num == len(data.get_bonded_atoms[k2])
        if k1num == 1 or k2num == 1:
            continue()
        #       check for imines
        if types[k1] == "N.2" and types[k2] == "N.2":
            continue

        #       check for double bonds based on bond types
        for ibond in range(0,nbonds):
            m1 = data.get_bonded_atoms[ibonds]


                 
      
		for $m (0 .. $#m_bonds){ 
			$m1=$m_bonds[$m]->[1];
			$m2=$m_bonds[$m]->[2];
			$m3=$m_bonds[$m]->[3];
			if(($k1==$m1&&$k2==$m2)||($k1==$m2&&$k2==$m1)){
				if($m3 ne '1'){
#uncomment for debug#			                print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- non-single bond (bond type $m3)\n";
			                next LABL;
				}
			}
		}
#       check for double bonds,based on the atom types : for the sake of safety
		if($t1 =~ /C\.2/ && $t2 =~ /C\.2/ ){
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- double bond\n";
			next LABL;
		}
#       check for triple bonds
		if($t1 =~ /C\.1/ && $t2 =~ /C\.1/ ){
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- triple bond\n";
			next LABL;
		}
#       check for amides
		if( ($t1 =~ /C\.2/ && $t2 =~ /N\.2|N\.am|N\.2|N\.pl3/) || ($t2 =~ /C\.2/ && $t1 =~ /N\.2|N\.am|N\.2|N\.pl3/) ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- amide\n";
			next LABL;
		}
#       check for planar amines
		if( ($t1 =~ /C/ && $spectypes{$k2} =~ 'planar_nh2') ||  ($t2 =~ /C/ && $spectypes{$k1} =~ 'planar_nh2') ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- planar amine\n";
			next LABL;
		}
#       check for methyls
		if( ($t1 =~ /.*/ && $spectypes{$k2} =~ 'methyl') ||  ($t2 =~ /.*/ && $spectypes{$k1} =~ 'methyl') ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- methyl\n";
			next LABL;
		}
#       check for aromatic amidines
		if( ($t1 =~ /C\.ar/ && $spectypes{$k2} =~ 'amidine') ||  ($t2 =~ /C\.ar/ && $spectypes{$k1} =~ 'amidine') ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- aromatic amidine\n";
			next LABL;
		}
#       check for aromatic sulfonate
		if( ($t1 =~ /C\.ar/ && $spectypes{$k2} =~ 'sulfonate') ||  ($t2 =~ /C\.ar/ && $spectypes{$k1} =~ 'sulfonate') ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- aromatic amidine\n";
			next LABL;
		}
#       check for aromatic nitro/nitroso
		if( ($t1 =~ /C\.ar/ && $spectypes{$k2} =~ 'nitro') ||  ($t2 =~ /C\.ar/ && $spectypes{$k1} =~ 'nitro') ) {
#uncomment for debug#			print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- aromatic nitro/nitroso\n";
			next LABL;
		}
#       check for aromatic carboxylic acid. The big question remains if C.ar-COOH is rotatable - V.K.
		if( ($t1 =~ /C\.ar/ && $spectypes{$k2} =~ 'carboxy') ||  ($t2 =~ /C\.ar/ && $spectypes{$k1} =~ 'carboxy') ) {
		#uncomment for debug#	print "Non-rotatable bond between $k1:$t1 and $k2:$t2 -- aromatic carboxylic acid\n";
			next LABL;
		}
#	the remaining bonds should be considered rotatable 
		push @keeplist,$k;
	}
#uncomment for debug#	print "keeplist [@keeplist]\n";

	my @rotlist=();
	foreach $i (@keeplist) {
		$tmp[0]=$m_bonds[$i][1];
		$tmp[1]=$m_bonds[$i][2];
		push @rotlist, [@tmp] ;
	}    
	for $i (0 .. $#rotlist){
		print "Rotatable bond: $rotlist[$i][0] --- $rotlist[$i][1]\n";
	}
	$n_rbonds=@rotlist;
	print STDERR "number of rotatable bonds $n_rbonds\n";

	close(MOL2FILE);
}

'''
