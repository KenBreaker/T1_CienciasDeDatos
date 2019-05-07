import csv
reader = csv.DictReader(open('OUTPUT/1D_output.csv', 'r'))
result = sorted(reader, key=lambda d: float(d['Cantidad_de_repeticiones']), reverse=True)
writer = csv.DictWriter(open('OUTPUT/1D_output_sorted.csv', 'w', newline=''), reader.fieldnames)
reader.close()
writer.writeheader()
writer.writerows(result)
writer.close()
