class Product:

    def __init__(self, name:str, price:float, count:int) -> None:
        self.name = name
        self.price = price
        self.count = count

    def get_data_product(self):
        data = {
            "name":self.name,
            "price":self.price,
            "count":self.count
        }
        return data