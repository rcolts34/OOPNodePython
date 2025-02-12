import time
from account import SavingsAccount, HighInterestSavingsAccount, OverdraftCheckingAccount

class BankServices:
    """Bank services like applying interest and generating reports."""
    def __init__(self):
        self.accounts = []  # Holds all accounts in the system

    def add_account(self, account):
        """Add an account to the system."""
        self.accounts.append(account)
        print(f"Account {account.account_number} added to the system.")

    def apply_interest_to_savings(self):
        """Apply interest to all savings accounts."""
        print("\nApplying interest to savings accounts...")
        for account in self.accounts:
            if isinstance(account, (SavingsAccount, HighInterestSavingsAccount)):
                account.apply_interest()

    def generate_reports(self):
        """Generate a summary report of all accounts."""
        print("\n--- Bank Account Summary Report ---")
        for account in self.accounts:
            print(f"Account Number: {account.account_number}, "
                  f"Holder: {account.holder_name}, Balance: ${account.balance}")
        print("-----------------------------------")

def run_services():
    """Run bank services periodically."""
    # Initialize BankServices
    bank_services = BankServices()

    # Create sample accounts (this can be replaced by database or file reading later)
    savings = SavingsAccount("12345", "John Doe", 1000)
    high_interest_savings = HighInterestSavingsAccount("67890", "Alice Johnson", 5000)
    checking = OverdraftCheckingAccount("54321", "Jane Smith", 500)

    # Add accounts to BankServices
    bank_services.add_account(savings)
    bank_services.add_account(high_interest_savings)
    bank_services.add_account(checking)

    # Periodically run services
    while True:
        print("\nRunning scheduled bank services...")
        bank_services.apply_interest_to_savings()
        bank_services.generate_reports()

        # Wait for 30 seconds (adjust as needed)
        time.sleep(30)

if __name__ == "__main__":
    run_services()
