import json

class Wallet:

	def __init__(self):
		self.__balance = 0
		self.__transactions = []
		self.read_file()

	def get_balance(self) -> float:
		return self.__balance

	def get_transactions(self) -> list:
		return self.__transactions

	def read_file(self) -> dict:
		try: 
			file = open("wallet.json")
		except IOError:
			file = open("wallet.json", "w+")

		try: 
			data = json.load(file)
			self.__balance = data["balance"]
			self.__transactions = data["transactions"]
		except ValueError:
			data = {}
			self.__balance = 0
			self.__transactions = []

		return data

	def add_balance(self, amount:float) -> None:
		self.__balance += amount

	def save(self) -> None:
		data = {
			"balance": self.__balance,
			"transactions": self.__transactions
		}
		json_string = json.dumps(data)	
		file = open("wallet.json", "w+")

		file.write(json_string)
		file.close()
	
	def add_transaction(self, transaction) -> None:
		self.__transactions.append({
			"amount": transaction.get_amount(),
			"date": transaction.get_date()
		})
		self.add_balance(transaction.get_amount())
		self.save()
		