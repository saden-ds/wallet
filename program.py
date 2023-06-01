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

		for wish in self.wish_list.wish_list:
			if len(wish.name) > max_name_len:
				max_name_len = len(wish.name)
			if len(wish.date) > max_date_len:
				max_date_len = len(wish.date)

		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+')
		print(f'| Name{" "*(max_name_len-4)} | Date{" "*(max_date_len-4)} |')
		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+')

		for wish in self.wish_list.wish_list:
			print(f'| {wish.name}{" "*(max_name_len-len(wish.name))} | {wish.date} |')
		
		print(f'+{"-"*(max_name_len+2)}+{"-"*(max_date_len+2)}+')
			

	def print_wish(self, name:str) -> None:
		wish = self.wish_list.get_wish(name)
		if wish is None:
			print('Wish does not exist!')

		print('Wish data:')
		print(f'Wish name: {name}')
		print(f'Wish date: {wish.date}')
		print('\nWish product list:')
		for product in wish.products:
			print(f'Product name: {product.name} | Product price: {product.price} | Product count: {product.count}|')


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

	def __add_amount(self) -> None:
		amount = input("Write amount: ")
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
		print("5: Exit")

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

			self.__print_transactions(options)
		elif command == "3":
			self.__add_amount()
		elif command == "4":
			self.__print_transactions()
			date = input("Write a date of transaction witch you wont to delete: ")
			self.__delete_transaction(date)
		elif command == "5":
			return False
		input('Press Enter to continue...')
		return True



