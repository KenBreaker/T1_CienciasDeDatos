import csv


class Order(object):
    def __init__(self, order_id):
        self.order_id = order_id
        self.product_id = []

    def pair_exists(self, product_id1, product_id2):
        if product_id1 in self.product_id and product_id2 in self.product_id:
            return True
        return False


class Pair(object):
    def __init__(self, product_id1, product_id2):
        self.product_id1 = product_id1
        self.product_id2 = product_id2
        self.totalSales = 0


products = []
Orders = []
i = -1
aux = 0

# Lectura del archivo
try:
    file = open("INPUT/order_products__train.csv", "r")
    file.readline()
    for line in file:
        data = line.split(",")
        if data[0] != aux:
            i = i + 1
            Orders.append(Order(data[0]))
            aux = data[0]
        if data[0] == aux:
            Orders[i].product_id.append(data[1])
            aux = data[0]
    file.close()
    print("Lectura de INPUT/order_products_train.csv finalizada")
except FileNotFoundError:
    print("El archivo INPUT/order_products_train.csv no existe")
    exit(-1)

for k in Orders:
    # print("order id", k.order_id ,"product id", k.product_id) Toda la info esta guardada en Orders
    # Se crea una lista solo con los productos para facilitar el computo
    length = len(k.product_id)
    for x in range(length):
        products.append(int(k.product_id[x]))
print("Lista productos finalizada")

output = open("OUTPUT/1D_output.csv", "w")
output.write("id_Producto,Cantidad_de_repeticiones\n")
    
# Se eliminan duplicados para evitar comparar reiteradas veces el mismo numero
myList = list(dict.fromkeys(products))
# print(len(mylist)) # cantidad de productos diferentes
length = len(myList)
for i in range(length):
    # print(str(mylist[i]) + "," + str(products.count(mylist[i])) + "\n")
    # Se cuenta la cantidad de repeticiones de cada palabra
    output.write(str(myList[i]) + "," + str(products.count(myList[i])) + "\n")
output.close()
print("Escritura en 1D_output finalizada")

reader = csv.DictReader(open('OUTPUT/1D_output.csv', 'r'))
result = sorted(reader, key=lambda d: float(d['Cantidad_de_repeticiones']), reverse=True)
writer = csv.DictWriter(open('OUTPUT/1D_output_sorted.csv', 'w', newline=''), reader.fieldnames)
writer.writeheader()
writer.writerows(result)
print("Escritura en 1D_output_sorted finalizada")

Pairs = []
products = []
try:
    file = open("OUTPUT/1D_output_sorted.csv", "r")
    file.readline()
    i = 0
    for line in file:
        data = line.split(",")
        # Si los productos comienzan a tener menor a 1000 ventas se ignorarán para el análisis 2D
        if int(data[1]) < 1000:
            break
        products.append(int(data[0]))
        i = i + 1
    file.close()
    print("Lectura de 1D_output_sorted finalizada")
except FileNotFoundError:
    print("El archivo OUTPUT/1D_output_sorted.csv no existe")
    exit(-1)

lengthProducts = len(products)
pos = 0
for i in range(lengthProducts):
    for j in range(i, lengthProducts):
        if products[i] != products[j]:
            Pairs.append(Pair(products[i], products[j]))
            for k in Orders:
                if k.pair_exists(products[i], products[j]):
                    Pairs[pos].totalSales += 1
            if Pairs[pos].totalSales == 0:
                Pairs.pop(pos)
            else:
                pos = pos + 1
print("Calculo de pares finalizado")

Pairs.sort(key=lambda paircito: paircito.totalSales, reverse=True)
print("Ordenamiento de pares finalizado")

output = open("OUTPUT/2D_output.csv", "w")
output.write("id_Producto1,id_Producto2,Cantidad_de_repeticiones\n")
for pair in Pairs:
    output.write(str(pair.product_id1) + "," + str(pair.product_id2) + "," + str(pair.totalSales) + "\n")
print("Escritura de OUTPUT/2D_output.csv finalizado")
