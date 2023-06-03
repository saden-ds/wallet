from wallet import Wallet
from transaction import Transaction
from os import system
import time
from operator import itemgetter

from wish_list import Wishlist

class Program:
	
	@staticmethod
	def run():
		program = Program()

		system('clear')
		print("Hello, this is your e-wallet. Let's start use it!")
		time.sleep(3)
		system('clear')
		
		while True:
			system('clear')
			program.__show_balance()
			program.__show_menu()

			if not program.__choose_command():
				program.wish_list.save()
				system('clear')
				print("Bye, Bye!")
				time.sleep(3)
				system('clear')
				break

	def __init__(self):
		self.wallet = Wallet()
		self.wish_list = Wishlist('detailed_wish_list.json', 'wish_list.json')


	def print_wishes(self) -> None:

		max_name_len = 5
		max_date_len = 5
		max_fullprice_len = 10

		for wish in self.wish_list.wish_list:
			if len(wish.name) > max_name_len:
				max_name_len = len(wish.name)
			if len(wish.date) > max_date_len:
				max_date_len = len(wish.date)
			if len(str(wish.fullprice)) > max_fullprice_len:
				max_fullprice_len = len(str(wish.fullprice))

		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+{"-"*(max_fullprice_len+2)}+')
		print(f'| Name{" "*(max_name_len-4)} | Date{" "*(max_date_len-4)} | Full price{" "*(max_fullprice_len-9)}|')
		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+{"-"*(max_fullprice_len+2)}+')

		for wish in self.wish_list.wish_list:
			print(f'| {wish.name}{" "*(max_name_len-len(wish.name))} | {wish.date}{" "*(max_date_len-len(wish.date))} | {str(wish.fullprice)}{" "*(max_fullprice_len-len(str(wish.fullprice)))} |')
		
		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+{"-"*(max_fullprice_len+2)}+')
			

	def print_wish(self, name:str) -> None:
		wish = self.wish_list.get_wish(name)
		if wish is None:
			print('Wish does not exist!')

		print('Wish data:')
		print(f'Wish name: {name}')
		print(f'Wish date: {wish.date}')
		print('\nWish product list:')

		max_product_name_len = 13
		max_product_price_len = 13
		max_product_count_len = 13

		for product in wish.products:
			if len(product.name) > max_product_name_len:
				max_product_name_len = len(product.name)
			if len(str(product.price)) > max_product_price_len:
				max_product_price_len = len(str(product.price))
			if len(str(product.count)) > max_product_count_len:
				max_product_count_len = len(str(product.count))
		print(f'+{"-"*(max_product_name_len+2)}+{"-"*(max_product_price_len+2)}+{"-"*(max_product_count_len+2)}+')
		print(f'| Product name {" "*(max_product_name_len - 13)} | Product price {" "*(max_product_price_len-13)}| Product count {" "*(max_product_count_len-13)}|')
		print(f'+{"-"*(max_product_name_len+2)}+{"-"*(max_product_price_len+2)}+{"-"*(max_product_count_len+2)}+')
		for product in wish.products:
			print(f'| {product.name + " "*(max_product_name_len-len(product.name))} | {str(product.price)+ " "*(max_product_price_len-len(str(product.price)))} | {str(product.count) + " "*(max_product_count_len- len(str(product.count)))} |')
		print(f'+{"-"*(max_product_name_len+2)}+{"-"*(max_product_price_len+2)}+{"-"*(max_product_count_len+2)}+')

	def __filter_transactions(self, transactions:list, options:dict = {}) -> list:
		options.setdefault('filter_column', None);
		options.setdefault('filter_command', None);
		options.setdefault('filter_value', None);

		if options['filter_column'] == None:
			return transactions

		filtered_transactions = [];

		for transaction in transactions:
			if options['filter_column'] == 'date':
				if transaction['date'] < options['filter_value'] + ' 00:00:00' or transaction['date'] > options['filter_value'] + ' 23:59:59':
					continue

			if options['filter_column'] == 'amount':
				if options['filter_command'] == '<=':
					if transaction['amount'] > options['filter_value']:
						continue
				elif options['filter_command'] == '>=':
					if transaction['amount'] < options['filter_value']:
						continue

				filtered_transactions.append(transaction)

		return filtered_transactions

	def __sort_transactions(self, transactions:list, options:dict = {}) -> list:
		options.setdefault('order', 'asc');
		options.setdefault('order_column', None)

		if options['order_column'] == 'date':
			transactions = sorted(transactions, key=itemgetter('date'), reverse = options['order'] == 'desc')
		elif options['order_column'] == 'amount':
			transactions = sorted(transactions, key=itemgetter('amount'), reverse = options['order'] == 'desc')

		return transactions

	def __print_transactions(self, options:dict = {}) -> None:
		transactions = self.wallet.get_transactions()
		total = 0
		
		transactions = self.__filter_transactions(transactions, options)
		transactions = self.__sort_transactions(transactions, options)

		if transactions:
			system('clear')
			print("Transactions")
			print("+ - - - - - - - - - - + - - - - - - +")
			print("| Date".ljust(22, " ") +  "|" +  "Amount".rjust(11, " ") +  "  |")
			print("+ - - - - - - - - - - + - - - - - - +")
			for transaction in transactions:
				amount = float(transaction['amount'])
				total += amount;
				print("| " + str(transaction['date']) + " | " + "{:.2f}".format(amount).rjust(10, " ") + "  |")
				print("+ - - - - - - - - - - + - - - - - - +")

		print("| Total:".ljust(22, " ") + "|" + str("{:.2f}".format(total)).rjust(12, " ") + " |")
		print("+ - - - - - - - - - - + - - - - - - +")
		print("")

	def __add_amount(self, amount) -> None:
		transaction = Transaction()
		transaction.set_amount(float(amount))
		if transaction.save(self.wallet):
			print(amount + " added to wallet!")
		else:
			print(transaction.get_error())

	def __delete_transaction(self, date:str) -> None:
		if self.wallet.delete_transaction(date):
			print("Transaction " + date + " was successfully deleted!")
		else:
			print("Transaction " + date + " not found!")

	def __show_balance(self) -> None:
		print("+ - - - - - - - - - - + - - - - - - +")
		print("| Balance:".ljust(22, " ") + "|" + str("{:.2f}".format(self.wallet.get_balance())).rjust(12, " ") + " |")
		print("+ - - - - - - - - - - + - - - - - - +")

	def __show_menu(self) -> None:
		print("Please select an action")
		print("1: Show transactions")
		print("2: Sort / Filter transactions")
		print("3: Add amount")
		print("4: Delete transaction")
		print("5: Show all wishes")
		print("6: Show specific wish")
		print("7: Sort / Filter wishes")
		print("8: Add wish")
		print("9: Use wish")
		print("10: Delete wish")
		print("11: Exit")

	def __choose_command(self) -> bool:
		
		command = input("Command: ")

		if command == "1":
			self.__print_transactions()
		elif command == "2":
			options = {
				"order": "asc",
				"order_column": None,
				"filter_column": None,
				"filter_command": None,
				"filter_value": None
			}

			print("How do you want to sort transactions")
			print("1: date ascending")
			print("2: date descending")
			print("3: amount ascending")
			print("4: amount descending")

			sort = input("Sort: ")

			if sort == "1":
				options['order'] = 'asc'
				options['order_column'] = 'date'
			elif sort == "2":
				options['order'] = 'desc'
				options['order_column'] = 'date'
			elif sort == "3":
				options['order'] = 'asc'
				options['order_column'] = 'amount'
			elif sort == "4":
				options['order'] = 'desc'
				options['order_column'] = 'amount'
			else:
				return True 

			print("Filter transactions by")
			print("1: date")
			print("2: amout less then")
			print("3: amout greater then")
			print("4: none")
			
			filt = input("Filter: ")

			if filt == "1":
				options['filter_column'] = 'date'
				options['filter_value'] =  input("Date: ")
			elif filt == "2":
				options['filter_column'] = 'amount'
				options['filter_command'] = '<='
				options['filter_value'] =  int(input("Amount less then: "))
			elif filt == "3":
				options['filter_column'] = 'amount'
				options['filter_command'] = '>='
				options['filter_value'] =  int(input("Amount greater then: "))
			else:
				return True

			self.__print_transactions(options)
		elif command == "3":
			amount = input("Write amount: ")
			
			if amount.strip() == "":
				return True

			self.__add_amount(amount)
		elif command == "4":
			self.__print_transactions()
			date = input("Write a date of transaction witch you wont to delete: ")
			
			if date.strip() == "":
				return True

			self.__delete_transaction(date)
		elif command == "5":
			system('clear')
			self.print_wishes()
		elif command == "6":
			system('clear')
			self.print_wishes()
			choice = input("Enter wish name to see details: ")
			if self.wish_list.get_wish(choice) is None:
				print("Wish does not exist!")
			else:
				system('clear')
				self.print_wish(choice)

		elif command == "7":
			pass
	
		elif command == "8":
			system('clear')

			while True:
				wish_name = input("Enter wish name: ")
				if wish_name.strip() == "":
					print("Incorrect name. Try again!")
					continue
				break
				
			products = []
			while True:
				product_name = input("Enter product name (if you want to stop adding products, press Enter):")
				product_price = 0
				product_count = 0
				if product_name.strip() == "":
					break
				while True:
					product_price = input("Enter product price: ")
					try:
						product_price = float(product_price)
					except:
						print("That is not float value. Try again!")
						continue
					break
				while True:
					product_count = input("Enter product count: ")
					try:
						product_count = int(product_count)
					except:
						print("That is not integer value. Try again!")
						continue
					break
				products.append(Wishlist.create_product(product_name, product_price, product_count))
			self.wish_list.create_and_add_wish(wish_name, products)

		elif command == "9":
			system('clear')
			self.print_wishes()
			choice = input("Enter wish name to use it: ")
			if self.wish_list.get_wish(choice) is None:
				print("Wish does not exist!")
			else:
				system('clear')
				wish = self.wish_list.get_wish(choice)
				self.__show_balance()
				print(f'Wish price: {wish.fullprice}')
				if self.wallet.get_balance() < wish.fullprice:
					print("You do not have enough money!")
				else:
					print("You have enough money! Do you want to buy it?")
					print(f"After buying you will have {self.wallet.get_balance()-wish.fullprice}")
					self.wish_list.use_wish(choice, self.wallet)
			

		elif command == "10":
			system('clear')
			self.print_wishes()
			choice = input("Enter wish name to delete it: ")
			if self.wish_list.get_wish(choice) is None:
				print("Wish does not exist!")
			else:
				system('clear')
				self.wish_list.delete_wish(choice)
				print(f'Wish {choice} was successfully deleted!')


		elif command == "11":
			return False
		
		input('Press Enter to continue...')
		return True



