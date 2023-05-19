from wallet import Wallet
from transaction import Transaction
from os import system
import time

class Program:
	
	@staticmethod
	def run():
		program = Program()

		system('clear')
		print("Hello, this is your e-wallet. Let's start use it!")
		time.sleep(3)
		system('clear')
		
		while True:
			program.show_balance()
			program.show_menu()

			if not program.choose_command():
				system('clear')
				print("Bye, Bye!")
				time.sleep(3)
				system('clear')
				break

	def __init__(self):
		self.wallet = Wallet()

	def print_transactions(self, options = {}):
		transactions = self.wallet.get_transactions()
		total = 0

		options.setdefault('order', 'asc');
		options.setdefault('filter_column', None);
		options.setdefault('filter_command', None);
		options.setdefault('filter_value', None);

		if options['order'] == 'desc':
			transactions = transactions[::-1]

		if transactions:
			system('clear')
			print("Transactions")
			print("+ - - - - - - - - - - + - - - - - - +")
			print("| Date".ljust(22, " ") +  "|" +  "Amount".rjust(11, " ") +  "  |")
			print("+ - - - - - - - - - - + - - - - - - +")
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

				amount = float(transaction['amount'])
				total += amount;
				print("| " + str(transaction['date']) + " | " + "{:.2f}".format(amount).rjust(10, " ") + "  |")
				print("+ - - - - - - - - - - + - - - - - - +")

		print("| Total:".ljust(22, " ") + "|" + str("{:.2f}".format(total)).rjust(12, " ") + " |")
		print("+ - - - - - - - - - - + - - - - - - +")
		print("")

	def add_amount(self):
		amount = input("Write amount: ")
		transaction = Transaction()
		transaction.set_amount(float(amount))
		if transaction.save(self.wallet):
			print(amount + " added to wallet!")
		else:
			print(transaction.get_error())

	def show_balance(self):
		print("+ - - - - - - - - - - + - - - - - - +")
		print("| Balance:".ljust(22, " ") + "|" + str("{:.2f}".format(self.wallet.get_balance())).rjust(12, " ") + " |")
		print("+ - - - - - - - - - - + - - - - - - +")

	def show_menu(self):
		print("Please select an action")
		print("1: Show transactions")
		print("2: Sort / Filter transactions")
		print("3: Add amount")
		print("4: Exit")

	def choose_command(self):
		
		command = input("Command: ")

		if command == "1":
			self.print_transactions()
		if command == "2":
			options = {
				"order": "asc",
				"filter_column": None,
				"filter_command": None,
				"filter_value": None
			}

			print("How you want to sort transactions")
			print("1: asc")
			print("2: desc")

			sort = input("Sort: ")

			if sort == "1":
				options['order'] = 'asc'
			elif sort == "2":
				options['order'] = 'desc'

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

			self.print_transactions(options)
		elif command == "3":
			self.add_amount()
		elif command == "4":
			return False

		return True



