from wallet import Wallet
from transaction import Transaction
from os import system

class Program:
	
	@staticmethod
	def run():
		program = Program()
		
		while True:
			program.show_balance()
			program.show_menu()

			if not program.choose_command():
				break

	def __init__(self):
		self.wallet = Wallet()

	def print_transactions(self):
		transactions = self.wallet.get_transactions()
	
		if transactions:
			system('clear')
			print("Transactions")
			print("+ - - - - - - - - - - + - - - - - - +")
			print("| Date".ljust(22, " ") +  "|" +  "Amount".rjust(11, " ") +  "  |")
			print("+ - - - - - - - - - - + - - - - - - +")
			for transaction in transactions:
				amount = float(transaction['amount'])
				print("| " + str(transaction['date']) + " | " + "{:.2f}".format(amount).rjust(10, " ") + "  |")
				print("+ - - - - - - - - - - + - - - - - - +")

	def add_amount(self):
		amount = input("Write amount: ")
		transaction = Transaction()
		transaction.set_amount(float(amount))
		if transaction.save(self.wallet):
			print(amount + " added to wallet!")
		else:
			print(transaction.get_errors())

	def show_balance(self):
		print("+ - - - - - - - - - - + - - - - - - +")
		print("| Balance:".ljust(22, " ") + "|" + str("{:.2f}".format(self.wallet.get_balance())).rjust(12, " ") + " |")
		print("+ - - - - - - - - - - + - - - - - - +")

	def show_menu(self):
		print("Please select an action")
		print("1: Show transactions")
		print("2: Add amount")
		print("3: Exit")

	def choose_command(self):
		command = input("Command: ")

		if command == "1":
			self.print_transactions()
		elif command == "2":
			self.add_amount()
		elif command == "3":
			return False

		return True



