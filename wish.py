from product import Product

class Wish:
    def __init__(self, name:str, date, products:list(Product)) -> None:
        self.name = name
        self.date = date
        self.products = products

    def get_json_products(self):
        return [product.get_json_product() for product in self.products]

    def get_json_wish(self):
        data = {
            "name":self.name,
            "date": self.date,
            "products": self.get_json_products()
        }
        return data
