import csv
class CsvSaver():    
    def __init__(self, name='jobs.csv'):
        self._name = name

    def create_file(self, columns):
        f = open(self._name, 'w')
        csv_file = csv.writer(f)
        csv_file.writerow(columns)
        f.close()

    def save_batch(self, rows):
        f = open(self._name, 'a')
        csv_file = csv.writer(f)
        for row in rows:
            csv_file.writerow(row.values())
        f.close()

    def save_links(self, rows):
        f = open('links_'+self._name, 'w')
        csv_file = csv.writer(f)
        for row in rows:
            csv_file.writerow([row])
        f.close()
