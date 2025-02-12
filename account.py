class Account:
      """"Base call for a generic account"""
      def __init__(self, account_number, holder_name, balance =0):
            self.account_number = account_number
            self.holder_name = holder_name
            self.balance = balance
            
      
      def deposit(self, amount):
            if amount > 0:
                  self.balance += amount
                  print(f"Deposited ${amount}. New balance: ${self.balance}")
            else:
                  print("Deposit amount must be positive")
                  
                  
      def withdraw(self, amount):
            if amount > 0 and amount <= self.balance:
                  self.balance -= amount
                  print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                  print("Insufficient Funds")
                  
                  
      def display_balance(self):
            print(f"Account Balance: ${self.balance}")
      
           
class SavingsAccount(Account):
            """Savings Account with Interest"""
            def __init__(self, account_number, holder_name, balance=0, interest_rate=0.01):
                  super().__init__(account_number, holder_name, balance)
                  self.interest_rate = interest_rate
            
            def apply_interest(self):
                  interest = self.balance * self.interest_rate
                  self.balance += interest
                  print(f"applied ${interest} interest. New balance: ${self.balance}")
         
                  
class CheckingAccount(Account):
      """Checking Account with no interest"""
      pass


class HighInterestSavingsAccount(SavingsAccount):
      """Savings Account with a higher interest rate"""
      def __init__(self, account_number, holder_name, balance=0, interest_rate=0.05):
            super().__init__(account_number, holder_name, balance)
            self.interest_rate = interest_rate
            

class OverdraftCheckingAccount(CheckingAccount):
      """Checking Account with overdraft protection"""
      def __init__(self, account_number, holder_name, balance=0, overdraft_limit=500):
            super().__init__(account_number, holder_name, balance)
            self.overdraft_limit = overdraft_limit
            
            
      def withdraw(self, amount):
            if amount > 0 and amount <= (self.balance + self.overdraft_limit):
                  self.balance -= amount
                  print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                  print("Withdrawl exceeds overdraft limit or is invalid")
                  
class PremiumOverdraftCheckingAccount(OverdraftCheckingAccount):
      """Premium account with cashback"""
      def __init__(self, account_number, holder_name, balance=0, overdraft_limit=500, cashback_rate=0.01):
            super().__init__(account_number, holder_name, balance, overdraft_limit)
            self.cashback_rate = cashback_rate
            
      def deposit(self, amount):
            super().deposit(amount)
            cashback = amount * self.cashback_rate
            self.balance += cashback
            print(f"Cashback earned ${amount}. New balance: ${self.balance}")