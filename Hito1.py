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
    def __init__(self, product_1, product_2):
        self.product_1 = product_1
        self.product_2 = product_2
        self.totalSales = 0


class Product(object):
    def __init__(self, product_id, product_name):
        self.product_id = product_id
        self.product_name = product_name


ProductNames = []
products = []
Orders = []
idList = []
i = -1
aux = 0

# Lectura del archivo con las transacciones
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
            Orders[i].product_id.append( int(data[1]))
            aux = data[0]
    file.close()
    print("Lectura de INPUT/order_products_train.csv finalizada")
except FileNotFoundError:
    print("El archivo INPUT/order_products_train.csv no existe")
    exit(-1)

#output fpgrowth
try:
    file = open("OUTPUT/fpgrowth.csv", "w", encoding='utf-8')
    print("Escribir fpgrowth.csv")
    for order in Orders:
        file.write(str(order.order_id))
        for product in range(len(order.product_id)):
            file.write(","+str(order.product_id[product]))
        file.write("\n")
    file.close()
    print("Finalizo escritura fpgrowth.csv")
except FileNotFoundError:
    print("No se pudo escribir en fpgrowth.csv")
    exit(-1)


# Lectura de los productos para obtener su nombre
try:
    file = open("INPUT/products.csv", "r", encoding='utf-8')
    file.readline()
    for line in file:
        data = line.split(",")
        ProductNames.append(Product(data[0], data[1].replace(",", " ").replace('"', '').replace("'", "")))
    file.close()
    print("Lectura de INPUT/products.csv finalizada")
except FileNotFoundError:
    print("El archivo INPUT/products.csv no existe")
    exit(-1)

prom_prod = 0
# Se crea una lista solo con los productos para facilitar el computo y se calcula la media de productos por transacción
for k in Orders:
    # print("order id", k.order_id ,"product id", k.product_id) Toda la info esta guardada en Orders
    length = len(k.product_id)
    prom_prod += length
    for x in range(length):
        products.append(k.product_id[x])
    # Se eliminan los duplicados para evitar redundancia
    # print(len(mylist)) # cantidad de productos diferentes
prom_prod /= len(Orders)
print("Lista de productos finalizada")

idList = list(dict.fromkeys(products))

# Se crea archivo con información varia
output = open("OUTPUT/info.csv", "w", encoding='utf-8')
output.write("Cantidad de ordenes: " + str(len(Orders)) + "\n")
output.write("Cantidad de productos: " + str(len(idList)) + "\n")
output.write("Media de productos por transacción: " + str(int(prom_prod)) + "\n")
output.close()
print("Escritura del archivo OUTPUT/info.csv finalizada")

# Se crea archivo para el análisis 1D
output = open("OUTPUT/1D_output.csv", "w", encoding='utf-8')
output.write("id_Producto,Nombre_producto,Cantidad_de_repeticiones\n")
    
# Se eliminan duplicados para evitar comparar reiteradas veces el mismo numero
# myList = list(dict.fromkeys(products))

length = len(idList)
# Se escribe en CSV la ID del producto con su nombre, y su cantidad de ventas
for i in range(length):
    # print(str(mylist[i]) + "," + str(products.count(mylist[i])) + "\n")
    name = "Missing"
    for x in ProductNames:
        if idList[i] == x.product_id:
            name = x.product_name
            break
    output.write(str(idList[i]) + "," + name + "," + str(products.count(idList[i])) + "\n")
output.close()
print("Escritura en 1D_output finalizada")

reader = csv.DictReader(open('OUTPUT/1D_output.csv', 'r', encoding='utf-8'))
result = sorted(reader, key=lambda d: float(d['Cantidad_de_repeticiones']), reverse=True)
writer = csv.DictWriter(open('OUTPUT/1D_output_sorted.csv', 'w', encoding='utf-8', newline=''), reader.fieldnames)
writer.writeheader()
writer.writerows(result)
print("Escritura en 1D_output_sorted finalizada")

Pairs = []
products = []
try:
    file = open("OUTPUT/1D_output_sorted.csv", "r", encoding='utf-8')
    file.readline()
    i = 0
    for line in file:
        data = line.split(",")
        # Si los productos comienzan a tener menor a 500 ventas se ignorarán para el análisis 2D
        if int(data[2]) < 500:
            break
        products.append(Product(data[0], data[1]))
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
        if products[i].product_id != products[j].product_id:
            Pairs.append(Pair(products[i], products[j]))
            for k in Orders:
                if k.pair_exists(products[i].product_id, products[j].product_id):
                    Pairs[pos].totalSales += 1
            if Pairs[pos].totalSales == 0:
                Pairs.pop(pos)
            else:
                pos = pos + 1
print("Calculo de pares finalizado")

Pairs.sort(key=lambda paircito: paircito.totalSales, reverse=True)
print("Ordenamiento de pares finalizado")

output = open("OUTPUT/2D_output.csv", "w", encoding='utf-8')
output.write("id_Producto1,Nombre_producto_1,id_Producto2,Nombre_producto_2,Cantidad_de_repeticiones\n")
for pair in Pairs:
    output.write(str(pair.product_1.product_id) + "," +
                 pair.product_1.product_name + "," +
                 str(pair.product_2.product_id) + ","
                 + pair.product_2.product_name + "," +
                 str(pair.totalSales) + "\n")
output.close()
print("Escritura de OUTPUT/2D_output.csv finalizado")
