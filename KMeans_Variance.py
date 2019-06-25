import re
import time
import numpy as np

n_products = 39123              # Cantidad de productos únicos (Default: 39123)
ini_cluster = 20                # Cantidad de clusters con que se iniciará
products = {}


# List comprehension
def ClusterIndicesComp(clustNum, labels_array):
    return np.array([i for i, x in enumerate(labels_array) if x == clustNum])


# Lectura de transacciones del archivo OUTPUT/fpgrowth_train_input.csv
transactions = []
try:
    file = open("OUTPUT/fpgrowth_train_input.csv", "r")
    for line in file:
        line = re.sub(r'[^0-9,]', '', line).split(",")[1:]
        transaction = list(int(id_product) for id_product in line)
        transactions.append(transaction)
    file.close()
except FileNotFoundError:
    print("El archivo " + pathfile + " no existe")
    exit(-1)

# Lectura de productos
try:
    file = open("INPUT/products_train.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        line = line.strip("\n").split(",")
        products[int(line[0])] = line[1]
    file.close()
except FileNotFoundError:
    print("El archivo INPUT/products_train.csv no existe")
    exit(-1)

# Para cada cluster de 20 a 2 en pares
for i in range(ini_cluster, 1, -2):

    # Se inicializa matriz nula de transacciones
    amount_of_transactions = len(transactions)
    kmeans_input = np.full((amount_of_transactions, n_products), 0)         # Antes estaba como '0'

    # Se agregan los productos comprados de cada transacción en la matriz nula
    for j in range(amount_of_transactions):
        for product_id in transactions[j]:
            kmeans_input[j][product_id-1] = 1

    # Se ejecuta KMeans con la cantidad de clusters i
    clusters_array = np.zeros([n_clusters], dtype=np.int)
    print("Ejecutando KMeans con K=" + str(i) + "...")
    start = time.time()
    kmeans = KMeans(n_jobs=-1, n_clusters=i).fit(kmeans_input)
    end = time.time()
    print("KMeans finalizado.\nGenerando archivo de salida...")

    # Se genera archivo de salida
    file_clusters = open("OUTPUT/Kmeans/clusters_variance/clusters_split1_K_" + str(n_clusters) + ".csv", "w", encoding='utf-8')
    file_clusters.write("Tiempo de ejecución: " + str(end - start) + "\n")
    # Se calcula cantidad de elementos que tiene cada cluster
    for j in kmeans.labels_:
        clusters_array[j] += 1
    # Se escribe cantidad de elementos que tiene cada cluster
    for j in clusters_array:
        file_clusters.write(str(j) + "\n")
    file_clusters.write("\n")
    for j in range(len(clusters_array)):
        file_clusters.write("Cluster " + str(i) + "\n")
        for line in ClusterIndicesComp(j, kmeans.labels_):
            print(line)
            #file[line] = file[line].strip("[]")
            #file_clusters.write(id_to_name(file[line]) + "\n")
            # file_clusters.write(str(file[line]))
        #file_clusters.write("\n")

    # Terminar con lo comentado arriba para escribir las transacciones a los archivos.
    # Evaluar varianza de cada cluster con panda, DataFrame.
    # Seleccionar cluster con mayor varianza.
    # Reemplazar las transacciones de la lista 'transactions' por las transacciones de este cluster.
    # Repetir dentro del ciclo for hasta que llegue a 2 clusters.
    # NOTA: el calculo de la diversidad y confianza se hacen con el otro código. Solo hay que cambiarle las rutas y los params.