from wallet import Wallet
from datetime import date, datetime

class Transaction:

	def __init__(self):
		now = datetime.now()
		self.__amount = 0
		self.__date = now.strftime("%Y-%m-%d %H:%M:%S")
		self.__error = ''

	def set_amount(self, amount) -> None:
		if isinstance(amount , str) and amount.strip('-').isnumeric():
			self.__amount = float(amount)
		else:
			self.__amount = amount

	def save(self, wallet = None) -> bool:
		if wallet == None:
			wallet = Wallet()

		self.validate()

		if not self.__error:
			balance = wallet.get_balance() + self.__amount 

			if balance < 0:
				self.__error = "Negative balance"

		if self.__error:
			return False
		
		wallet.add_transaction(self)
		return True

	def get_amount(self) -> float:
		return self.__amount 

	def get_date(self) -> str:
		return self.__date

	def get_error(self) -> str:
		return self.__error

	def validate(self) -> None:
		self.__error = ""

		if isinstance(self.__amount, float) != True and isinstance(self.__amount, int) != True:
			self.__error = "Amount must be a number"
			return None

		if self.__amount == 0:
			self.__error = "Amout must not be zero"
			return None 

 	