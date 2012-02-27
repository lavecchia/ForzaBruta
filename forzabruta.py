#!/usr/bin/env python
# forzabruta 30sep2010 v. 2.0.0
# algoritmo para generar conformaciones a partir de la variacion de parametros. El directorio debe contener:
# - archivo de geometria (pdb, xyz ...) Ejemplo. estructura.pdb
# - archivo de parametros (.in). Ejemplo. estructura.in.
#
# En este ultimo se listaran los diedros a modificar D atom1 atom2 atom3 atom4. Si se desea que un diedro varie entre
# valores en particular hagalo luego de esta forma: D atom1 atom2 atom3 atom4 = val1 val2 val3 val4 ...

import string
import os
import datetime
import sys
from pymol import cmd
import pymol
from optparse import OptionParser  

# extraido de http://doeidoei.wordpress.com/2009/02/11/pymol-api-simple-example/
import __main__ 
__main__.pymol_argv = [ 'pymol', '-qcr'] # Quiet and no GUI
pymol.finish_launching()

#VARIABLES
variaciondef = [-60,60,180] #rango por defecto
atomIDs = [] #almacena los Id de los atomos a modificar los parametros
paramod = [] #almacen parametros modificables 
matrizval = [] #almacena por cada columna los valores respectivos para cada archivo de salida


#PARSEO
usage = "%prog [opciones]"
parser = OptionParser(usage=usage, version="%prog 1.0")
parser.add_option('-i','--infile', action='store', type ='string', dest='infile', metavar='nombre', help='especifica el nombre de la entrada\n')
parser.add_option('-r','--rango', action='store', type ='string', dest='variacion', metavar='rango', help='rango de variacion de parametro. por defecto "-60 60 120" \n')
#parser.add_option('-p','--param', action='store', type ='string', dest='parametros', metavar='parametros', help='especifica archivo con parametros a modificar. por defecto nombreentrada.in" \n')
(options, args) = parser.parse_args()

# Especifica nombre de entrada	
if options.infile:
	structurefile = options.infile
else:
	print "Debe especificar un archivo de entrada. Ej. forzabruta -i ejemplo.pdb"
	sys.exit()

# Especifica variacion
if options.variacion:
	variacion = options.variacion.split()
else:
	variacion = variaciondef

# Especifica archivo con parametros
#if options.variacion:
#	infilename = options.parametros
#else:
#	infilenamediv = structurefile.split(".")
#	infilename = infilenamediv[0]+ ".in"
infilenamediv = structurefile.split(".")
infilename = infilenamediv[0]+ ".in"

    
#CODIGO
#1. Genera Matriz con valores de diedros variables

pymol.cmd.load(os.path.abspath(os.curdir)+ "//" + structurefile)




infile = open(infilename,"r") #abre archivo con parametros a modificar

nroparam = 0
for line in infile:
	paramod.append([])
	linediv = line.split("=") #corta la linea
	line1div = linediv[0].split()
	if line1div[0] == "D":
		atom1 = line1div[1]
		atom2 = line1div[2]
		atom3 = line1div[3]
		atom4 = line1div[4]
	if len(linediv)>1:
		line2div = linediv[1].split()
		nrovalores=len(line2div) #calcula cuantos valores va a tomar este parametro
		if nrovalores > 0: #si existe algun valor...
			for valor in range(0,nrovalores):
				paramod[nroparam].append(line2div[valor])				
	else: #sino		
		paramod[nroparam]=variacion #asigna variacion por defecto
	atomIDs.append("ID " + atom1 + ", ID " + atom2 + ", ID " + atom3 + ", ID " + atom4) #guarda en atomIDs los atomos a modificar en cada linea
	nroparam = nroparam + 1
infile.close()
		
#2. Genera matriz matrizval nxm donde n es el numero de archivos a generar y m los parametros a modificar
nrosalidas=1
for n in range(0,len(paramod)):
	nrosalidas = nrosalidas*len(paramod[n])

if len(paramod)>0:
	print "Parametros a modificar: " + str(nroparam)
	print "Salidas a generar: " + str(nrosalidas)
	for n in range(0,nrosalidas):
		matrizval.append([])
	for npam in range(0,len(paramod)):
		nsal = 0
		for p in range(0,nrosalidas/len(paramod[npam])):
			for valor in paramod[npam]:
				matrizval[nsal].append(valor)
				nsal = nsal + 1
		matrizval.sort() #importante para el programa


	#3. Genera Archivos de Salidas
	infilenamediv=infilename.split(".")
	for nsal in range(0,nrosalidas):
		salida = [] #lista que contiene las lineas para un archivo de salida especifico
		npam = 0
		extname = infilenamediv[0]
		for line in atomIDs: 
			linediv=line.split(",")
			val = float(matrizval[int(nsal)][int(npam)])
			cmd.set_dihedral(linediv[0],linediv[1],linediv[2],linediv[3], val)
			#extname = extname + "_D" + linediv[0].strip("ID ")+"-"+linediv[1].strip("ID ")+"-"+linediv[2].strip("ID ")+"-"+linediv[3].strip("ID ") + "_" + str(int(val)) #nombre de salida con valores de parametros
			extname = extname + "_D" + str(npam) + "_" + str(int(val)) #nombre de salida con valores de parametros			
			npam = npam + 1
		cmd.save(extname+".pdb")
		print "Se creo el archivo " + extname+".pdb"
else:
	print "No se encuentran parametros para modificar"


# Get out!
pymol.cmd.quit()





	
