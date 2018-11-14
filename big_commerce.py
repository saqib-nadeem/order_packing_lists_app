class Parser:

    def get_orders_from_csv_file(self, path_to_csv):
        return [Order('Order ID: ' + str(i)) for i in range(3)]


class Order:

    def __init__(self, id):
        self.id = id

