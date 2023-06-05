from product import Product
from datetime import datetime

class Wish:
    def __init__(self, name:str, date:str, products:list[Product]) -> None:
        self.name = name
        self.fullprice = 0
        
        if len(date) == 0:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.date = date

        self.products = products

        self.calculate_fullprice()

    def calculate_fullprice(self):
        for product in self.products:
            self.fullprice += product.price * product.count

    # получение json структуры всех продуктов в желании (без json.dumps -> обычный dict).
    def get_data_products(self):
        return [product.get_data_product() for product in self.products]

    # получение json структуры всего желания (без json.dumps -> обычный dict).
    def get_data_wish(self):
        data = {
            "name":self.name,
            "date": self.date,
            "products": self.get_data_products()
        }
        return data
