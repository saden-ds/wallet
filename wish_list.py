from wish import Wish
import json

class Wishlist:

    def __init__(self, wish_list_file_path:str) -> None:
        self.__file_path = wish_list_file_path
        self.wish_list = []


    def add_wish(self, wish:Wish):
        self.wish_list.append(wish)

    def use_wish(self):
        pass

    def save(self):
        data = {"detailedWishList":[wish.get_json_wish() for wish in self.wish_list]}
        json_string = json.dumps(data)

        f = open(self.__file_path, 'w+')
        f.write(json_string)
        f.close()
