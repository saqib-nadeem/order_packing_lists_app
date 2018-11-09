import csv

class ComboParser:

    def parse(self, path):
        combos = {}
        combo_name = ''

        with open(path, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for index, row in enumerate(reader):
                if index == 0: continue

                combo_name = row[0].strip() or combo_name

                if combo_name not in combos:
                    combos[combo_name] = Combo(combo_name)

                combos[combo_name].combo_items.append(
                    ComboItem(row[2], row[3],row[4])
                )

        return combos



class Combo:

    def __init__(self, name):
        self.name = name
        self.combo_items = []
        
    
    def __str__(self):
        return '\n' + '\n'.join(str(item) for item in self.combo_items) + '\n\n'
        
        
    def __repr__(self):
        return str(self)


class ComboItem:

    def __init__(self, qty, sku, description):
        self.qty = qty
        self.sku = sku
        self.description = description


    def __str__(self):
        return 'ComboItem({0}, {1}, {2})'.format(self.qty, self.sku, self.description)
        
        
    def __repr__(self):
        return str(self)
        



if __name__ == '__main__':
    combos = ComboParser().parse('files/combos_steaks.csv')
    print(combos)



