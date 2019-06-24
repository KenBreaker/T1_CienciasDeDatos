transactions = []
transaction_id = []
products_train = []
products = {}
products_new_id = {}
products_train_pair = {}
new_id = 1

# Se guarda en lista todas las transacciones del archivo fpgrowth_input.csv
try:
    file = open("OUTPUT/fpgrowth_input.csv", "r")
    file2 = open("OUTPUT/fpgrowth_train_input.csv", "w")
    for line in file:
        line = line.split(",")
        transaction_id.append(line[0])
        line = line[1:]
        transaction = list(int(i) for i in line)
        transactions.append(transaction)
    file.close()
except FileNotFoundError:
    print("El archivo OUTPUT/fpgrowht_input.csv no existe")
    exit(-1)
print("Transacciones leídas")

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
print("Productos leídos")

for transaction in transactions:
    for product_id in transaction:
        if product_id not in products_train:
            products_train.append(product_id)
            products_train_pair[new_id] = products[product_id]
            products_new_id[product_id] = new_id
            new_id += 1
print("Productos en train generados")

for i in range(0, len(transactions)):
    for j in range(0, len(transactions[i])):
        transactions[i][j] = products_new_id[transactions[i][j]]

file = open("INPUT/products_train.csv", "w", encoding='utf-8')
file.write("product_id,product_name\n")
for key, value in products_train_pair.items():
    file.write(str(key) + "," + value + "\n")
file.close()
print("Productos train escritos")

file = open("OUTPUT/fpgrowth_train_input.csv", "w")
for i in range(0, len(transactions)):
    file.write(str(transaction_id[i]))
    for product_id in transactions[i]:
        file.write("," + str(product_id))
    file.write("\n")
file.close()
print("Nuevo fpgrowth_input escrito")