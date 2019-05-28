import pyfpgrowth
import time

transactions = []                   # Lista de transacciones
products = {}                       # Directorio de los productos
support_threshold = 3              # Mínimo soporte permitido
min_confidence = 0.7                # Mínima confianza permitida
max_transactions = 10000000         # Cantidad máxima de transacciones a procesar


# Transforma una lista de ID en una variable con los nombres de los productos.
def id_to_name(id_list):
    id_list = str(id_list).replace("(", "").replace(")", "").split(",")
    name_list = []
    for i in range(0, len(id_list) - 1):
        name_list.append(products[int(id_list[i])])
    name_list = sorted(name_list, key=lambda x: x.replace(" ", ""))
    names = name_list[0]
    for i in range(1, len(name_list)):
        names += ", " + name_list[i]
    return names


# Se guarda en lista todas las transacciones del archivo fpgrowth_input.csv
try:
    file = open("OUTPUT/fpgrowth_input.csv", "r")
    number_of_transactions = 0
    for line in file:
        if number_of_transactions >= max_transactions:
            break
        line = line.split(",")
        transaction = list(int(i) for i in line)
        transactions.append(transaction)
        number_of_transactions += 1
    file.close()
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowht_input.csv no existe")
    exit(-1)

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
    exit(-1)

# Se generan patrones frecuentes dado un mínimo de soporte
start = time.time()
patterns = pyfpgrowth.find_frequent_patterns(transactions, support_threshold)
'''
filename = "OUTPUT/FP_Growth/frequent_patterns_" + str(support_threshold) + "S.csv"
file = open(filename, "w", encoding='utf-8')
for key, value in patterns.items():
    # print(str(key) + ": " + str(value))
    file.write("{" + id_to_name(key) + "}: " + str(value) + "\n")
file.close()
'''

# Se generan reglas de asociación dado un mínimo de confianza. La variable KEY es el antecedente, VALUE[0] es el consecuente, e VALUE[1] es la confianza
rules = pyfpgrowth.generate_association_rules(patterns, min_confidence)
end = time.time()
filename = "OUTPUT/FP_Growth/association_rules_" + str(support_threshold) + "S.csv"
file = open(filename, "w", encoding='utf-8')
for key, value in sorted(rules.items(), key=lambda kv: kv[1][1], reverse=True):
    if len(key) + len(value[0]) < 4:
        continue
    # print(str(key) + ": (" + str(value[0]) + ", " + str('%.3f'%float(value[1])) + ") =>" + str(len(key)+len(value[0])))
    file.write("{" + id_to_name(key) + "} => {" + id_to_name(value[0]) + "}: " + str('%.3f'%float(value[1])) + "\n")
file.close()

print("Tiempo para " + str(len(transactions)) +
      " transacciones, con S=" + str(support_threshold) +
      " y C=" + str(min_confidence) +
      " ====> " + str('%.5f' % float(end-start)) + " seg")
