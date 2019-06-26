from sklearn.cluster import KMeans
import re
import time
import numpy as np
import pandas as pd

n_products = 39123              # Cantidad de productos únicos (Default: 39123)
ini_cluster = 20                # Cantidad de clusters con que se iniciará
transaction_limit = 1000000     # Límite de transacciones a leer
products = {}
transactions = []


# List comprehension
def ClusterIndicesComp(clustNum, labels_array):
    return np.array([i for i, x in enumerate(labels_array) if x == clustNum])


# Transforma una lista de ID en una variable con los nombres de los productos.
def id_to_name(id_list):
    id_list = re.sub(r'[^0-9,]', '', str(id_list)).split(",")
    # id_list = str(id_list).strip("[]").replace(" ", "").replace("(", "").replace(")", "").replace("\n", "").split(",")
    name_list = []
    for i in range(0, len(id_list) - 1):
        name_list.append(products[int(id_list[i])])
    name_list = sorted(name_list, key=lambda x: x.replace(" ", ""))
    names = ""
    if len(name_list):
        names = re.sub(r'[^a-zA-Z0-9% ]', '', name_list[0])
    for i in range(1, len(name_list)):
        if len(name_list[i]):
            names += ", " + re.sub(r'[^a-zA-Z0-9% ]', '', name_list[i])
    return names

# Se crea matriz nula y se agregan los productos comprados a cada transacción
def prepare_matrix(_transactions):
    _amount_of_transactions = len(_transactions)
    _kmeans_input = np.full((_amount_of_transactions, n_products), 0)  # Antes estaba como '0'
    for x in range(_amount_of_transactions):
        for _product_id in _transactions[x]:
            _kmeans_input[x][_product_id - 1] = 1
    return _kmeans_input

# Lectura de transacciones del archivo OUTPUT/fpgrowth_train_input.csv
print("Leyendo transacciones...")
try:
    file = open("OUTPUT/fpgrowth_train_input.csv", "r")
    transaction_ct = 0
    for line in file:
        transaction_ct += 1
        if transaction_ct > transaction_limit:
            break
        line = re.sub(r'[^0-9,]', '', line).split(",")[1:]
        transaction = list(int(id_product) for id_product in line)
        transactions.append(transaction)
    file.close()
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowth_train_input.csv no existe")
    exit(-1)

# Lectura de productos
print("Leyendo productos...")
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

# Se prepara matriz nula y se le agregan los productos de cada transacción
kmeans_input = prepare_matrix(transactions)

# Para cada cluster de 20 a 2 en pares
for i in range(ini_cluster, 1, -2):

    # Se ejecuta KMeans con la cantidad de clusters i
    clusters_array = np.zeros([i], dtype=np.int)
    print("Ejecutando KMeans con K=" + str(i) + "... ", end='')
    start = time.time()
    kmeans = KMeans(n_jobs=-1, n_clusters=i).fit(kmeans_input)
    end = time.time()
    print("Finalizado. Generando archivo de salida...")

    # Se genera archivo de salida
    file_clusters = open("OUTPUT/Kmeans/clusters_variance/clusters_split1_K_" + str(i) + ".csv", "w", encoding='utf-8')
    file_clusters.write("Tiempo de ejecucion: " + str(end - start) + "\n")
    # Se calcula cantidad de elementos que tiene cada cluster
    for j in kmeans.labels_:
        clusters_array[j] += 1
    # Se escribe cantidad de elementos que tiene cada cluster
    for j in clusters_array:
        file_clusters.write(str(j) + "\n")
    file_clusters.write("\n")
    # Se escriben las transacciones de cada cluster al archivo, reemplanzando su ID por su nombre
    list_of_clusters = []
    for j in range(len(clusters_array)):
        file_clusters.write("Cluster " + str(j) + "\n")
        transactions_in_cluster = []        # Se crea lista de transacciones en cada cluster
        for line in ClusterIndicesComp(j, kmeans.labels_):
            file_clusters.write(id_to_name(transactions[line]).replace("\n", "") + "\n")
            transactions_in_cluster.append(transactions[line])
        list_of_clusters.append(transactions_in_cluster)
        file_clusters.write("\n")

    # Se prepara la nueva matriz de transacciones para cada cluster
    for j in range(len(list_of_clusters)):                                  # Número del cluster
        amount_in_cluster = len(list_of_clusters[j])
        transactions_matrix = np.full((amount_in_cluster, n_products), 0)
        for k in range(amount_in_cluster):                                  # Número de la transacción en cluster
            for product_id in list_of_clusters[j][k]:                       # ID del producto en transacción
                transactions_matrix[k][product_id-1] = 1
        list_of_clusters[j] = transactions_matrix
        # print(str(list_of_clusters[j]) + "\n")

    # Se calcula la varianza de cada cluster
    df = []
    length_cluster = len(list_of_clusters)
    variance_in_cluster = [0.0 for x in range(length_cluster)]
    for j in range(length_cluster):
        df.append(pd.DataFrame(list_of_clusters[j]))
        for variance in df[j].var(axis=1):
            #print(variance)
            variance_in_cluster[j] += float(variance)
        variance_in_cluster[j] /= n_products

    '''
    for j in range(length_cluster):
        print("Cluster " + str(j) + ": " + str(variance_in_cluster[j]))
    '''

    # Se selecciona el cluster con mayor varianza y se preparan variables para siguiente iteración (K = K-2)
    index_of_max_element = 0
    greater_value = variance_in_cluster[0]
    for j in range(1, length_cluster):
        if greater_value < variance_in_cluster[j]:
            greater_value = variance_in_cluster[j]
            index_of_max_element = j
    kmeans_input = list_of_clusters[index_of_max_element]
    transactions = []

    # Se genera una nueva lista de transacciones con ID
    for j in range(len(kmeans_input)):
        transaction_with_id = []
        for k in range(len(kmeans_input[j])):
            if kmeans_input[j][k]:
                transaction_with_id.append(k+1)
        transactions.append(transaction_with_id)

    # print(str(index_of_max_element) + " | " + str(transactions))

    # NOTA: el calculo de la diversidad y confianza se hacen con el otro código. Solo hay que cambiarle las rutas y los params.