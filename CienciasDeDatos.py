from itertools import groupby
from collections import Counter
file = open("database/order_products__train.csv","r")
data = []
i = -1
products = []
class Order(object):
  def __init__(self, order_id):
    self.order_id = order_id
    self.product_id = []

Orders = []
file.readline()
aux = 0
#Lectura del archivo
for line in file:
    data = line.split(",")
    if (data[0] != aux):
        i = i + 1
        Orders.append(Order(data[0]))
        aux = data[0]
    if (data[0] == aux ):
        Orders[i].product_id.append(data[1])
        aux = data[0]


for k in Orders:
    #print("order id", k.order_id ,"product id", k.product_id) Toda la info esta guardada en Orders
    for x in range (len(k.product_id)):
    # Se crea una lista solo con los productos para facilitar el computo
        products.append(int(k.product_id[x]))

#Se crea archivo de salida
output = open("output.csv","w")
output.write("id_Producto,Cantidad_de_repeticiones\n")

#Se eliminan duplicados para evitar comparar reiteradas veces el mismo numero
mylist = list( dict.fromkeys(products))
#print(len(mylist)) cantidad de productos diferentes
for i in range (len(mylist)):
    #print(str(mylist[i])+","+str(products.count(mylist[i]))+"\n")
    output.write(str(mylist[i])+","+str(products.count(mylist[i]))+"\n") #Se cuenta la cantidad de repeticiones de cada palabra