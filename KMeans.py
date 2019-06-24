from sklearn.cluster import KMeans
import numpy as np
import random
import time
import sys
transacctions = []
kmeans_array = []
kmeans_input = []
id_max = 0
lines = 0
id_split = 1
n_lineas =500
n_clusters = 2

n_productos=49688

# Read, Randomize & Split
try:
    print("Lectura de OUTPUT/fpgrowth_input.csv Inicializada")
    file = open("OUTPUT/fpgrowth_input.csv", "r").readlines()
    random.shuffle(file)
    for line in file:
        if (lines==0):
            file_split = open("OUTPUT/Kmeans/splits/split_"+str(id_split)+".csv","w+")
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


try:

    for n_split in range (1,id_split):
        file = open("OUTPUT/Kmeans/splits/split_"+str(n_split)+".csv", "r").readlines()
        i = 0
        print("Inicializando matriz")
        kmeans_input = np.full((len(file),n_productos), '0')
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
        while(n_clusters<=20):
            clusters_array = np.zeros([n_clusters], dtype=np.int)
            print("Ejecutando Kmeans K = "+str(n_clusters)+ " Split = "+str(n_split))
            start = time.time()
            kmeans = KMeans(n_clusters=n_clusters).fit(kmeans_input)
            end = time.time()
            print("Finalizo Kmeans")
            print("Creando archivo OUTPUT")
            file_clusters = open("OUTPUT/Kmeans/clusters/clusters_split" + str(n_split) + "_K_"+str(n_clusters) +".csv", "w+")
            file_clusters.write(str(end - start) + "\n")
            for i in kmeans.labels_:
                clusters_array[i] = clusters_array[i]  +  1
            for i in clusters_array:
                file_clusters.write(str(i)+"\n")
            n_clusters = n_clusters + 2
            print("OUTPUT Finalizado")
            file_clusters.close()

    '''
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
    '''
except FileNotFoundError:
    print("El archivo OUTPUT/Kmeans/splits/split_"+str(n_split)+".csv"+" no existe")
    exit(-1)


