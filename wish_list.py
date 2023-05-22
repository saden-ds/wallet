from wish import Wish
import json
from product import Product
from wallet import Wallet

class Wishlist:

    def __init__(self, wish_list_file_path:str, wish_list_short_file_path:str) -> None:
        self.__short_file_path = wish_list_short_file_path
        self.__file_path = wish_list_file_path
        self.wish_list = self.read_file()

    # добавление желания в список.
    def add_wish(self, wish:Wish):
        self.wish_list.append(wish)

    # создание желания и добавление его в список.
    def create_and_add_wish(self, name:str, products:list[Product]):
        wish = Wish(name, '', products)
        self.add_wish(wish)

    # создание продукта (static method)
    @staticmethod
    def create_product( name:str, price:float, count:int):
        product = Product(name, price, count)
        return product

    def get_wish(self, name:str) -> Wish:
        for w in self.wish_list:
            if w.name == name:
                return w
        return None

    # использование какого то желания (после применения оно удаляется).
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


    # обычное сохранение полной структуры в файл self.__file_path (путь до подробного описания).
    # сохранение укороченной структуры в файл self.__short_file_path (путь до укороченного описания).
    def save(self):
        #детальное сохранение в файл self.__file_path
        data = {"detailedWishList":[wish.get_data_wish() for wish in self.wish_list]}
        json_string = json.dumps(data, indent=4)
        
        f = open(self.__file_path, 'w')
        f.write(json_string)
        f.close()

        # укороченное сохранение в файл self.__short_file_path.
        data = {"shortWishList": [{"name":wish.name, "date":wish.date} for wish in self.wish_list]}
        json_string = json.dumps(data, indent=4)
        
        f = open(self.__short_file_path, 'w')
        f.write(json_string)
        f.close()


    # создание всего объекта считывая файл self.__file_path (полная структура).
    def read_file(self):

        # попытка открыть файл. Если его нет, то создать новый.
        try:
            f = open(self.__file_path)
        except IOError:
            f = open(self.__file_path, "w+")
            f.close()
            return []

        # попытка переобразовать json файл в структуру самого класса Wishlist. Если выдаёт ошибку (файл self.__file_path 
        # повреждён: json структура сохранена неверно и другие ошибки записи), то создается пустой объект Wishlist.
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