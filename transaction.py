from wallet import Wallet
from datetime import date, datetime

class Transaction:

	def __init__(self):
		now = datetime.now()
		self.amount = 0
		self.date = now.strftime("%Y-%m-%d %H:%M:%S")
		self.error = ''

	def set_amount(self, amount):
		self.amount = amount 

	def set_date(self, date):
		self.date = date 

	def save(self, wallet = None):
		if wallet == None:
			wallet = Wallet()

		self.validate()

		if not self.error:
			balance = wallet.get_balance() + self.amount 

			if balance < 0:
				self.error = "Negative balance"

		if self.error:
			return False
		
		wallet.add_transaction(self)
		return True

	def get_amount(self):
		return self.amount 

	def get_date(self):
		return self.date

	def get_error(self):
		return self.error

	def validate(self):
		self.error = ""

		if isinstance(self.amount, float) != True and isinstance(self.amount, int) != True:
			self.error = "Amount must be float or integer"
			return None

		if self.amount == 0:
			self.error = "Amout must not be zero"
			return None 

 	