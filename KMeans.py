from sklearn.cluster import KMeans
import numpy as np
import random
import sys
transacctions = []
kmeans_array = []
kmeans_input = []
id_max = 0
lines = 0
id_split = 1
n_lineas = 2000
# Read, Randomize & Split
try:
    print("Lectura de OUTPUT/fpgrowth_input.csv Inicializada")
    file = open("OUTPUT/fpgrowth_input.csv", "r").readlines()
    random.shuffle(file)
    for line in file:
        if (lines==0):
            file_split = open("OUTPUT/Kmeans/split_"+str(id_split)+".csv","w+")
            print("Split #" + str(id_split) + " Finalizado")
            id_split = id_split + 1
        line = line.split(",")[1:]
        transaction = list(int(i) for i in line)
        file_split.write( str(transaction)+"\n" )
        lines = lines + 1
        if (lines== n_lineas):
            lines=0
    print("Lectura de OUTPUT/fpgrowth_input.csv finalizada")
    #kmeans_array = np.array(transacctions)
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowth_input.csv no existe")
    exit(-1)

#ARFF File
try:
    file = open("OUTPUT/Kmeans/split_"+str(1)+".csv", "r").readlines()
    i = 0
    print("Inicializando matriz")
    kmeans_input = np.full((n_lineas,49688), '0')
    print("Matriz nula lista")
    print("Agregando productos a la matriz")
    for line in file:
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.split(",")
        for idProduct in line:
            kmeans_input[i][ (int(idProduct)-1)] = 1
        i = i + 1
    print("Matriz finalizada")
    file.close()
    print("Generando archivo ARFF")
    file_clusters = open("OUTPUT/Kmeans/kmeans_clusters.arff", "w+")
    file_clusters.write("@relation productos\n\n")
    for i in range(49688):
        file_clusters.write("@attribute " + "producto" + str(i) + " {0,1}\n")
    file_clusters.write("\n@data\n")
    for line in kmeans_input:
        for i in line:
            file_clusters.write(str(i)+",")
        file_clusters.write("\n")
    print("Archivo Creado")
    file_clusters.close()
except FileNotFoundError:
    print("El archivo OUTPUT/Kmeans/split_"+str(1)+".csv"+" no existe")
    exit(-1)

    #print("Ejecutando Kmeans")
    #kmeans = KMeans(n_clusters=2).fit(kmeans_input)
    #print("Finalizo Kmeans")

