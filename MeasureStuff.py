import math
import re
import pyfpgrowth

n_split = 1                                    # Cantidad máxima de splits
n_cluster = 10                                  # Cantidad máxima de clusters
entropy = []                                    # Cada posición es la entropía (de Shannon) de un split
confidence = []                                 # Cada posición es la confianza de un split
products = {}                                   # Colección de productos con nombre (key) y su ID


# Escritura de la cantidad de clusters en el header
def write_cluster_header(file_header):
    for i in range(2, n_cluster, 2):
        file_header.write(";" + i)
    file_header.write("\n")


results = open("OUTPUT/KMeans_results.csv", "w", encoding='utf-8')
write_cluster_header(results)

# Calculo de la entropía promedio de cada split
for i in range(n_split):
    entropy.append(0.0)
    results.write(str(i) + ";")
    for j in range(2, n_cluster + 1, 2):
        amount_of_transactions = 0
        clusters = []
        try:
            file = open("OUTPUT/Kmeans/clusters/clusters_split" + str(i+1) + "_K_" + str(j) + ".csv", "r", encoding='utf-8')
            file.readline()
            for k in range(j):
                line = file.readline()
                amount_in_cluster = int(line)
                clusters.append(amount_in_cluster)
                amount_of_transactions += amount_in_cluster
            file.close()
        except FileNotFoundError:
            print("No se pudo encontrar el archivo OUTPUT/Kmeans/clusters_split" + str(i+1) + "_K_" + str(j) + ".csv")
            continue
        for k in range(j):
            probability = clusters[k] / amount_of_transactions
            entropy[i] -= (probability * math.log(probability, 2))
    entropy[i] /= n_cluster

for i in range(n_split):
    print("Entropía promedio split " + str(i + 1) + " = " + str('%.3f'%float(entropy[i])))
print("Entropía promedio total = " + str('%.3f'%float(sum(entropy) / n_split)) + "\n")

# Lectura de productos con su respectivo nombre
try:
    file = open("INPUT/products_train.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        line = line.split(",")
        product_name = re.sub(r'[^a-zA-Z0-9% ]', '', line[1]).replace("\n", "")
        products[product_name] = int(line[0])
    file.close()
except FileNotFoundError:
    print("El archivo INPUT/products.csv no existe")
    exit(-1)

#Calculo de confianza promedio de cada split. Solo se considera mayor cluster en cada split.
for i in range(n_split):
    confidence.append(0.0)
    for j in range(2, n_cluster + 1, 2):
        clusters = []
        try:
            file = open("OUTPUT/Kmeans/clusters/clusters_split" + str(i + 1) + "_K_" + str(j) + ".csv", "r", encoding='utf-8')
            file.readline()
            # Guarda la cantidad de transacciones en cada cluster
            for k in range(j):
                line = file.readline()
                clusters.append(int(line))
            index_of_max_element = clusters.index(max(clusters))
            # Lee archivo hasta encontrar sección del cluster con más transacciones
            for line in file:
                line = line.replace("\n", "")
                if line == str("Cluster " + str(index_of_max_element)):
                    break
            transactions = []  # Matriz de transacciones para FP-Growth
            # Transforma el nombre de cada producto a su ID y almacena el resultado
            for line in file:
                # Si llega al siguiente cluster,
                line = line.replace("\n", "")
                if line == str("Cluster " + str(index_of_max_element + 1)):
                    break
                if len(line):
                    line = line.split(", ")
                    transaction = []
                    for product in line:
                        if len(product):
                            transaction.append(products[product])
                    transactions.append(transaction)
            file.close()
        except FileNotFoundError:
            print("No se pudo encontrar el archivo OUTPUT/Kmeans/clusters/clusters_split" + str(i + 1) + "_K_" + str(j) + ".csv")
            continue
        # Se generan patrones frecuentes dado un mínimo soporte de 6
        patterns = pyfpgrowth.find_frequent_patterns(transactions, 6)
        # Se generan reglas de asociación con confianza mínima del 50%
        rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
        # Se promedia la confianza de las reglas de asociación obtenidas. VALUE[1] corresponde a la confianza
        confidence_cluster = 0.0
        for key, value in rules.items():
            confidence_cluster += float(value[1])
            # print(str(key) + " => " + str(value[0]) + " | " + str('%.3f'%float(value[1])))
        # print("Cantidad de reglas: " + str(len(rules)) + "\n")
        confidence[i] += (confidence_cluster / len(rules))
    confidence[i] /= (n_cluster / 2)

for i in range(n_split):
    print("Confianza promedio split " + str(i + 1) + " = " + str('%.3f'%float(confidence[i])))
print("Confianza promedio total = " + str('%.3f'%float(sum(confidence) / n_split)))
