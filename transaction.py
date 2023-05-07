from wallet import Wallet
from datetime import date, datetime

class Transaction:

	def __init__(self):
		now = datetime.now()
		self.amount = 0
		self.date = now.strftime("%Y-%m-%d %H:%M:%S")
		self.errors = {}

	def set_amount(self, amount):
		self.amount = amount 

	def set_date(self, date):
		self.date = date 

	def save(self, wallet = None):
		if wallet == None:
			wallet = Wallet()

		self.validate()

		if self.errors:
			return False
		else:
			wallet.add_transaction(self)

		return True

	def get_amount(self):
		return self.amount 

	def get_date(self):
		return self.date

	def get_errors(self):
		return self.errors

	def validate(self):
		self.errors = {}

		if isinstance(self.amount, float) != True and isinstance(self.amount, int) != True:
			self.errors["amount"] = "Must be float or integer"
		elif self.amount == 0:
			self.errors["amount"] = "Must not be zero"

		if isinstance(self.date , str) != True:
			self.errors["date"] = "Must be string"
		else:
			self.validate_date()

	def validate_date(self):
		try:
			datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")
		except ValueError:
			self.errors["date"] = "Invalid date format, must be Y-m-d"

        


 	