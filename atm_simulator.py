import sys
import getpass
from datetime import datetime

class ATMSimulator:
    def __init__(self, initial_balance=1000, pin='1234', max_attempts=3):
        """
        Initialize the ATM with default or custom settings.
        
        :param initial_balance: Starting account balance
        :param pin: Account PIN
        :param max_attempts: Maximum PIN entry attempts
        """
        self._balance = initial_balance
        self._pin = pin
        self._max_attempts = max_attempts
        self._transaction_history = []
    
    def _log_transaction(self, transaction_type, amount):
        """
        Log transaction details for account tracking.
        
        :param transaction_type: Type of transaction (deposit/withdrawal)
        :param amount: Transaction amount
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'balance': self._balance,
            'timestamp': timestamp
        }
        self._transaction_history.append(transaction)
    
    def authenticate(self):
        """
        Authenticate user with PIN verification.
        
        :return: Boolean indicating successful authentication
        """
        attempts = 0
        while attempts < self._max_attempts:
            try:
                # Using getpass to hide PIN input
                entered_pin = getpass.getpass("Please enter your PIN: ")
                
                if entered_pin == self._pin:
                    print("Authentication successful!")
                    return True
                
                attempts += 1
                remaining = self._max_attempts - attempts
                print(f"Invalid PIN. {remaining} attempt{'s' if remaining != 1 else ''} remaining.")
            
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return False
        
        print("Too many invalid attempts. Account locked.")
        return False
    
    def check_balance(self):
        """Display current account balance."""
        print(f"Your current balance is: ${self._balance:.2f}")
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        :param amount: Amount to deposit
        :return: Boolean indicating successful deposit
        """
        try:
            amount = float(amount)
            if amount <= 0:
                print("Invalid deposit amount. Please enter a positive value.")
                return False
            
            self._balance += amount
            self._log_transaction('deposit', amount)
            print(f"${amount:.2f} deposited successfully.")
            print(f"New balance: ${self._balance:.2f}")
            return True
        
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")
            return False
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        
        :param amount: Amount to withdraw
        :return: Boolean indicating successful withdrawal
        """
        try:
            amount = float(amount)
            if amount <= 0:
                print("Invalid withdrawal amount. Please enter a positive value.")
                return False
            
            if amount > self._balance:
                print("Insufficient funds!")
                return False
            
            self._balance -= amount
            self._log_transaction('withdrawal', amount)
            print(f"${amount:.2f} withdrawn successfully.")
            print(f"New balance: ${self._balance:.2f}")
            return True
        
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")
            return False
    
    def print_transaction_history(self):
        """Display account transaction history."""
        if not self._transaction_history:
            print("No transactions found.")
            return
        
        print("\n--- Transaction History ---")
        for transaction in self._transaction_history:
            print(f"{transaction['timestamp']} | "
                  f"Type: {transaction['type'].capitalize()} | "
                  f"Amount: ${transaction['amount']:.2f} | "
                  f"Balance: ${transaction['balance']:.2f}")
    
    def run(self):
        """Main ATM simulation loop."""
        if not self.authenticate():
            sys.exit(1)
        
        while True:
            try:
                print("\n--- ATM Menu ---")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Transaction History")
                print("5. Exit")
                
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.check_balance()
                elif choice == '2':
                    amount = input("Enter amount to deposit: $")
                    self.deposit(amount)
                elif choice == '3':
                    amount = input("Enter amount to withdraw: $")
                    self.withdraw(amount)
                elif choice == '4':
                    self.print_transaction_history()
                elif choice == '5':
                    print("Thank you for using the ATM. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                break

def main():
    """Entry point for the ATM simulator."""
    atm = ATMSimulator()
    atm.run()

if __name__ == "__main__":
    main()