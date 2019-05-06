import csv
reader = csv.DictReader(open('output.csv', 'r'))
result = sorted(reader, key=lambda d: float(d['Cantidad_de_repeticiones']))
writer = csv.DictWriter(open('output_sorted.csv', 'w'), reader.fieldnames)
writer.writeheader()
writer.writerows(result)