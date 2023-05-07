import json

class Wallet:

	def __init__(self):
		self.balance = 0
		self.transactions = []
		self.read_file()

	def get_balance(self):
		return self.balance

	def get_transactions(self):
		return self.transactions

	def read_file(self):
		try: 
			file = open("wallet.json")
		except IOError:
			file = open("wallet.json", "w+")

		try: 
			data = json.load(file)
			self.balance = data["balance"]
			self.transactions = data["transactions"]
		except ValueError:
			data = {}
			self.balance = 0
			self.transactions = []

		return data

	def add_balance(self, amount):
		self.balance += amount

	def save(self):
		data = {
			"balance": self.balance,
			"transactions": self.transactions
		}
		json_string = json.dumps(data)	
		file = open("wallet.json", "w+")

		file.write(json_string)
		file.close()
	
	def add_transaction(self, transaction):
		self.transactions.append({
			"amount": transaction.get_amount(),
			"date": transaction.get_date()
		})
		self.add_balance(transaction.get_amount())
		self.save()
		