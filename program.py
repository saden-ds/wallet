from wallet import Wallet
from transaction import Transaction
from os import system
from datetime import date, datetime
import time
from operator import itemgetter
from operator import attrgetter

from wish_list import Wishlist

class Program:
	
	@staticmethod
	def run():
		program = Program()
		system('clear')
		print("Hello, this is your e-wallet. Let's start using it!")
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

	def __get_max_len(self, max_len, value):
		value_len = len(str(value))
		
		if value_len > max_len:
			max_len = value_len
	
		return max_len

	def __column_separator(self, column_len:int) -> str:
		return "-" * (column_len + 2)

	def __column(self, column_value:str, column_len:int, right:bool = False) -> str:
		if right:
			return " " + str(column_value).rjust(column_len, " ") + " "
		else:
			return " " + str(column_value).ljust(column_len, " ") + " "

	def print_wishes(self, wishList) -> None:

		max_name_len = 5
		max_date_len = 5
		max_fullprice_len = 10

		for wish in wishList:
			if len(wish.name) > max_name_len:
				max_name_len = len(wish.name)
			if len(wish.date) > max_date_len:
				max_date_len = len(wish.date)
			if len(f'{wish.fullprice:.2f}') > max_fullprice_len:
				max_fullprice_len = len(f'{wish.fullprice:.2f}')

		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+{"-"*(max_fullprice_len+2)}+')
		print(f'| Name{" "*(max_name_len-4)} | Date{" "*(max_date_len-4)} | Full price{" "*(max_fullprice_len-9)}|')
		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+{"-"*(max_fullprice_len+2)}+')

		for wish in wishList:
			print(f"| {wish.name}{' '*(max_name_len-len(wish.name))} | {wish.date}{' '*(max_date_len-len(wish.date))} | {wish.fullprice:.2f}{' '*(max_fullprice_len-len(f'{wish.fullprice:.2f}'))} |")
		
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
			if len(f'{product.price:.2f}') > max_product_price_len:
				max_product_price_len = len(f'{product.price:.2f}')
			if len(str(product.count)) > max_product_count_len:
				max_product_count_len = len(str(product.count))
		print(f'+{"-"*(max_product_name_len+2)}+{"-"*(max_product_price_len+2)}+{"-"*(max_product_count_len+2)}+')
		print(f'| Product name {" "*(max_product_name_len - 13)} | Product price {" "*(max_product_price_len-13)}| Product count {" "*(max_product_count_len-13)}|')
		print(f'+{"-"*(max_product_name_len+2)}+{"-"*(max_product_price_len+2)}+{"-"*(max_product_count_len+2)}+')
		for product in wish.products:
			print(f'| {product.name + " "*(max_product_name_len-len(product.name))} | {f"{product.price:.2f}"+ " "*(max_product_price_len-len(f"{product.price:.2f}"))} | {str(product.count) + " "*(max_product_count_len- len(str(product.count)))} |')
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

	def __get_transactions_total(self, transactions):
		total = 0

		if transactions:
			for transaction in transactions:
				amount = float(transaction['amount'])
				total += amount;

		return total

	def __print_sorted_filtered_wishes(self, sort_option:int, filter_option:int):
		temp_wishlist = self.wish_list.wish_list[:]
		if sort_option == 1:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('name'))
		elif sort_option == 2:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('name'), reverse=True)
		elif sort_option == 3:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('date'))
		elif sort_option == 4:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('date'), reverse=True)
		elif sort_option == 5:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('fullprice'))
		elif sort_option == 6:
			temp_wishlist = sorted(temp_wishlist, key = attrgetter('fullprice'), reverse=True)
		
		if filter_option == 1:
			contains = input("Enter name or part of name: ")
			for wish in temp_wishlist[:]:
				if wish.name.count(contains) == 0:
					temp_wishlist.remove(wish)
		elif filter_option == 2:
			date = input("Enter date: ")
			for wish in temp_wishlist[:]:
				if not wish.date.split(" ")[0] == date:
					temp_wishlist.remove(wish)
		elif filter_option == 3:
			while True:
				price = 0
				try:
					price = float(input("Enter price: "))
					if price <= 0:
						print('Price has to be positive integer or float!')
						continue

				except:
					print('Price has to be positive integer or float!')
					continue
				break

			for wish in temp_wishlist[:]:
				if wish.fullprice > price:
					temp_wishlist.remove(wish)

		elif filter_option == 4:
			while True:
				price = 0
				try:
					price = float(input("Enter price: "))
					if price <= 0:
						print('Price has to be positive integer or float!')
						continue

				except:
					print('Price has to be positive integer or float!')
					continue
				break

			for wish in temp_wishlist[:]:
				if wish.fullprice < price:
					temp_wishlist.remove(wish)
		system("clear")
		self.print_wishes(temp_wishlist)

	def __print_transactions(self, options:dict = {}) -> None:
		system('clear')

		transactions = self.wallet.get_transactions()
		date_name = "Date"
		amount_name = "Amount"
		date_len = len(date_name)
		amount_len = len(amount_name)

		transactions = self.__filter_transactions(transactions, options)

		transactions = self.__sort_transactions(transactions, options)
		total = self.__get_transactions_total(transactions)

		amount_len = self.__get_max_len(amount_len, "{:.2f}".format(total))

		if transactions:
			for transaction in transactions:
				date_len = self.__get_max_len(date_len, transaction["date"])
				amount_len = self.__get_max_len(amount_len, "{:.2f}".format(transaction["amount"]))

		print("Transactions")
		print(f'+{self.__column_separator(date_len)}+{self.__column_separator(amount_len)}+')
		print(f'|{self.__column(date_name, date_len)}|{self.__column(amount_name, amount_len, True)}|')
		print(f'+{self.__column_separator(date_len)}+{self.__column_separator(amount_len)}+')

		if transactions:
			for transaction in transactions:
				amount = float(transaction['amount'])
				print(f'|{self.__column(transaction["date"], date_len)}|{self.__column("{:.2f}".format(amount), amount_len, True)}|')
				print(f'+{self.__column_separator(date_len)}+{self.__column_separator(amount_len)}+')

			print(f'|{self.__column("Total", date_len)}|{self.__column("{:.2f}".format(total), amount_len, True)}|')
			print(f'+{self.__column_separator(date_len)}+{self.__column_separator(amount_len)}+')
		else:
			print(f'+{self.__column_separator(date_len)}+{self.__column_separator(amount_len)}+')

		print("")

	def __add_amount(self, amount) -> None:
		transaction = Transaction()
		transaction.set_amount(amount)
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
		balance = "{:.2f}".format(self.wallet.get_balance())
		balance_len = len(str(balance))
		name_len = 10
		print(f'+{self.__column_separator(name_len)}+{self.__column_separator(balance_len)}+')
		print(f'|{self.__column("Balance:", name_len)}|{self.__column(balance, balance_len, True)}|')
		print(f'+{self.__column_separator(name_len)}+{self.__column_separator(balance_len)}+')

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
		print("11: Save & Exit")

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

			system('clear')

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
				options['filter_value'] =  input("Date (example " + datetime.now().strftime("%Y-%m-%d") + "): ")
			elif filt == "2":
				options['filter_column'] = 'amount'
				options['filter_command'] = '<='
				options['filter_value'] =  int(input("Amount less then: "))
			elif filt == "3":
				options['filter_column'] = 'amount'
				options['filter_command'] = '>='
				options['filter_value'] =  int(input("Amount greater then: "))
			elif filt != "4":
				return True

			self.__print_transactions(options)
		elif command == "3":
			amount = input("Write amount: ")
			
			if amount.strip() == "":
				return True

			self.__add_amount(amount)
		elif command == "4":
			self.__print_transactions()
			date = input("Write the date of the transaction you want to delete: ")
			
			if date.strip() == "":
				return True

			self.__delete_transaction(date)
		elif command == "5":
			system('clear')
			self.print_wishes(self.wish_list.wish_list)
		elif command == "6":
			system('clear')
			self.print_wishes(self.wish_list.wish_list)
			choice = input("Enter wish name to see details: ")
			if self.wish_list.get_wish(choice) is None:
				print("Wish does not exist!")
			else:
				system('clear')
				self.print_wish(choice)

		elif command == "7":
			sort_option = 0
			filter_option = 0
			while True:
				system('clear')
				print('How do you want to sort wishes')
				print('1: Name ascending')
				print('2: Name descending')
				print('3: Date ascending')
				print('4: Date descending')
				print('5: Full price ascending')
				print('6: Full price descending')
				try:
					sort_option = int(input('Sort: '))
					if sort_option > 6 or sort_option < 1:
						print('Input has to be number between 1-6')
						input('Press Enter to continue...')
						continue
				
				except:
					print('Input has to be number between 1-6')
					input('Press Enter to continue...')
					continue
				break
			
			while True:
				system('clear')
				print('How do you want to filter wishes')
				print('1: Name')
				print('2: Date')
				print('3: Full price less then')
				print('4: Full price greater then')
				try:
					filter_option = int(input('Filter: '))
					if filter_option > 4 or filter_option < 1:
						print('Input has to be number between 1-4')
						input('Press Enter to continue...')
						continue
				
				except:
					print('Input has to be number between 1-4')
					input('Press Enter to continue...')
					continue
				break
			self.__print_sorted_filtered_wishes(sort_option, filter_option)

	
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
						if product_price <= 0:
							print("The product price must be positive!")
							continue
					except:
						print("That is not float value. Try again!")
						continue
					break
				while True:
					product_count = input("Enter product count: ")
					try:
						product_count = int(product_count)
						if product_count <= 0:
							print("The product count must be positive!")
							continue
					except:
						print("That is not integer value. Try again!")
						continue
					break
				products.append(Wishlist.create_product(product_name, product_price, product_count))
			if len(products) < 1:
				print("The wish has to contain at least one product!")
			else:
				self.wish_list.create_and_add_wish(wish_name, products)

		elif command == "9":
			system('clear')
			self.print_wishes(self.wish_list.wish_list)
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
			self.print_wishes(self.wish_list.wish_list)
			choice = input("Enter wish name to delete it: ")
			if self.wish_list.get_wish(choice) is None:
				print("Wish does not exist!")
			else:
				system('clear')
				self.wish_list.delete_wish(choice)
				print(f'Wish {choice} was successfully deleted!')


		elif command == "11":
			return False
		else:
			print("Incorrect input!")
		input('Press Enter to continue...')
		return True
