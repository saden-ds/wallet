from product import Product

class Wish:
    def __init__(self, name:str, date:str, products:list[Product]) -> None:
        self.name = name
        self.date = date
        self.products = products

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
