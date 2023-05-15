from wish import Wish
import json
from product import Product
from wallet import Wallet

class Wishlist:

    def __init__(self, wish_list_file_path:str) -> None:
        self.__file_path = wish_list_file_path
        self.wish_list = self.read_file()


    def add_wish(self, wish:Wish):
        self.wish_list.append(wish)

    def use_wish(self, name:str, wallet:Wallet):
        wish = None
        wish_index = 0
        for w in self.wish_list:
            if w.name == name:
                wish = w
                break
            wish_index+=1

        if wish is None:
            return 0
        
        wish_price = 0.0

        for product in wish.products:
            wish_price += product.price
        if wallet.balance < wish_price:
            return 0
        
        wallet.balance -= wish_price
        self.wish_list.remove(wish)

    def save(self):
        data = {"detailedWishList":[wish.get_data_wish() for wish in self.wish_list]}
        json_string = json.dumps(data)
        
        f = open(self.__file_path, 'w')
        f.write(json_string)
        f.close()

    def read_file(self):
        try:
            f = open(self.__file_path)
        except IOError:
            f = open(self.__file_path, "w+")
            return []


        try:
            data = json.load(f)
            data = data["detailedWishList"]
            res = []

            for wish in data:
                products = []
                for product in wish["products"]:
                    products.append(Product(product["name"], product["price"], product["count"]))
                res.append(Wish(wish["name"], wish["date"], products))
            return res
        
        except ValueError:
            return []