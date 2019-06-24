from sklearn.cluster import KMeans
import numpy as np
import random
import time
import pandas
import sys
transacctions = []
kmeans_array = []
kmeans_input = []
id_max = 0
lines = 0
id_split = 1
<<<<<<< HEAD
n_lineas =2000
n_clusters = 2
products = {}
n_productos=49688

# Se guarda el nombre de los productos
try:
    file = open("INPUT/products.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        line = line.split(",")
        products[int(line[0])] = line[1]
    file.close()
except FileNotFoundError:
    print("El archivo INPUT/products.csv no existe")
=======
n_lineas = 3000
n_clusters = 2
products = {}
n_productos=39123

# Se guarda el nombre de los productos
try:
    file = open("INPUT/products_train.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        line = line.strip("\n").split(",")
        products[int(line[0])] = line[1]
    file.close()
except FileNotFoundError:
    print("El archivo INPUT/products_train.csv no existe")
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
    exit(-1)

# Transforma una lista de ID en una variable con los nombres de los productos.
def id_to_name(id_list):
<<<<<<< HEAD
    id_list = str(id_list).replace("(", "").replace(")", "").split(",")
=======
    id_list = str(id_list).replace(" ","").strip("[]").replace("(", "").replace(")", "").replace("\n","").split(",")
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
    name_list = []
    for i in range(0, len(id_list) - 1):
        name_list.append(products[int(id_list[i])])
    name_list = sorted(name_list, key=lambda x: x.replace(" ", ""))
    names = ""
    if (len(name_list)):
        names = name_list[0]
    for i in range(1, len(name_list)):
        names += ", " + name_list[i]
    return names

<<<<<<< HEAD
# Se guarda el nombre de los productos
try:
    file = open("INPUT/products_train.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        line = line.split(",")
        products[int(line[0])] = line[1]
    file.close()
except FileNotFoundError:
    print("El archivo INPUT/products.csv no existe")
    exit(-1)

# Read, Randomize & Split
try:
    print("Lectura de OUTPUT/fpgrowth_input.csv Inicializada")
    file = open("OUTPUT/fpgrowth_input.csv", "r").readlines()
=======
# Read, Randomize & Split
try:
    print("Lectura de OUTPUT/fpgrowth_train_input.csv Inicializada")
    file = open("OUTPUT/fpgrowth_train_input.csv", "r").readlines()
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
    random.shuffle(file)
    for line in file:
        if (lines==0):
            file_split = open("OUTPUT/Kmeans/splits/split_"+str(id_split)+".csv","w")
            print("Split #" + str(id_split) + " Finalizado")
            id_split = id_split + 1
        line = line.split(",")[1:]
        transaction = list(int(i) for i in line)
        file_split.write( str(transaction)+"\n" )
        lines = lines + 1
        if (lines== n_lineas):
            lines=0
<<<<<<< HEAD
    print("Lectura de OUTPUT/fpgrowth_input.csv finalizada")
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowth_input.csv no existe")
=======
    print("Lectura de OUTPUT/fpgrowth_train_input.csv finalizada")
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowth_train_input.csv no existe")
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
    exit(-1)
def ClusterIndicesNumpy(clustNum, labels_array): #numpy
    return np.where(labels_array == clustNum)[0]

def ClusterIndicesComp(clustNum, labels_array): #list comprehension
    return np.array([i for i, x in enumerate(labels_array) if x == clustNum])

try:

<<<<<<< HEAD
    for n_split in range (1,2):
=======
    for n_split in range (1,id_split):
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
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
            k = 0
            for idProduct in line:
                #if k!=0:
                kmeans_input[i][ (int(idProduct)-1)] = 1
                #k = k + 1

            i = i + 1
        print("Matriz finalizada")

        while(n_clusters<=20):
            clusters_array = np.zeros([n_clusters], dtype=np.int)
            print("Ejecutando Kmeans K = "+str(n_clusters)+ " Split = "+str(n_split))
            start = time.time()
            kmeans = KMeans(n_clusters=n_clusters,precompute_distances= True).fit(kmeans_input)
            end = time.time()
            print("Finalizo Kmeans")
            print("Creando archivo OUTPUT")
            file_clusters = open("OUTPUT/Kmeans/clusters/clusters_split" + str(n_split) + "_K_"+str(n_clusters) +".csv", "w+", encoding='utf-8')
            file_clusters.write(str(end - start) + "\n")
            for i in kmeans.labels_:
                clusters_array[i] = clusters_array[i]  +  1
            k = 0
            for i in clusters_array:
                file_clusters.write(str(i))
                file_clusters.write("\n")
            file_clusters.write("\n")
            for i in range (len(clusters_array)):
                file_clusters.write("Cluster "+str(i)+"\n")
                for line in ClusterIndicesComp(k, kmeans.labels_):
<<<<<<< HEAD

                    file[line] = file[line].strip("[]")
                    file_clusters.write(str(id_to_name((file[line]))))

                file_clusters.write("\n")
                k = k + 1
=======
                    file[line] = file[line].strip("[]")
                    file_clusters.write(str(id_to_name(file[line])))
                    #file_clusters.write(str(file[line]))
                file_clusters.write("\n")
                k= k + 1

>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
            n_clusters = n_clusters + 2
            print("OUTPUT Finalizado")
            file_clusters.close()
except FileNotFoundError:
    print("El archivo OUTPUT/Kmeans/splits/split_"+str(n_split)+".csv"+" no existe")
    exit(-1)



'''        
        while(n_clusters<=20):
            clusters_array = np.zeros([n_clusters], dtype=np.int)
            print("Ejecutando Kmeans K = "+str(n_clusters)+ " Split = "+str(n_split))
            start = time.time()
            kmeans = KMeans(n_clusters=n_clusters,precompute_distances= True).fit(kmeans_input)
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
<<<<<<< HEAD
            print( ClusterIndicesNumpy(1, kmeans.labels_) )
=======

            print( ClusterIndicesNumpy(1, kmeans.labels_) )

>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
            print("OUTPUT Finalizado")
            file_clusters.close()
'''

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


'''
        print("Generando archivo RapidMiner")
        file_clusters = open("OUTPUT/Kmeans/kmeans_rapidminer.csv", "w")
        for line in kmeans_input:
            for i in line:
                file_clusters.write(str(i) + ",")
            file_clusters.write("\n")
        print("Archivo Creado")
<<<<<<< HEAD
'''
=======
'''
>>>>>>> caceb23e9c7f8f2b5c5a5efc85dc5db9ad361361
