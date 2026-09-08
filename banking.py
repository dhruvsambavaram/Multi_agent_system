class Account:
    """
    Represents a bank account that supports depositing, withdrawing, and transferring funds.
    """

    def __init__(self, name, initial_balance=0.0):
        self.name = name
        self.balance = initial_balance

    def deposit(self, amount):
        """
        Adds money to the account balance.
        
        Args:
            amount (float): Amount of money to deposit.
            
        Raises:
            ValueError: If the amount is negative.
        """
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative.")
        self.balance += amount
        print(f"Deposited ${amount:.2f} into {self.name}'s account. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        """
        Withdraws money from the account balance (crediting out).
        
        Args:
            amount (float): Amount of money to withdraw.
            
        Raises:
            ValueError: If the amount exceeds the current balance.
        """
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative.")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds for {self.name}. Current balance: ${self.balance:.2f}")
        self.balance -= amount
        print(f"Withdrew ${amount:.2f} from {self.name}'s account. New balance: ${self.balance:.2f}")

    def transfer(self, recipient_account, amount):
        """
        Transfers money from this account to the recipient account.
        
        Args:
            recipient_account (Account): The account to transfer funds to.
            amount (float): Amount of money to transfer.
            
        Raises:
            ValueError: If amount is negative or if the sender has insufficient funds.
        """
        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds for {self.name}. Current balance: ${self.balance:.2f}. Cannot transfer ${amount:.2f}.")
        
        self.balance -= amount
        recipient_account.balance += amount
        print(f"Transferred ${amount:.2f} from {self.name} to {recipient_account.name}.")
        print(f"{self.name} balance: ${self.balance:.2f}, {recipient_account.name} balance: ${recipient_account.balance:.2f}")


if __name__ == "__main__":
    # Create three user instances
    alice = Account("Alice", 1000.0)
    bob = Account("Bob", 0.0)
    charlie = Account("Charlie", 500.0)

    print("--- Account Creation ---")
    print(f"Alice Account Created with initial balance ${alice.balance:.2f}")
    print(f"Bob Account Created with initial balance ${bob.balance:.2f}")
    print(f"Charlie Account Created with initial balance ${charlie.balance:.2f}")
    print()

    print("--- Performing Deposit ---")
    alice.deposit(500.0)
    print()

    print("--- Performing Transfer ---")
    alice.transfer(bob, 300.0)
    print()

    print("--- Performing Withdrawal (Credit Out) ---")
    charlie.withdraw(200.0)
    print()

    print("--- Final Balances ---")
    print(f"Alice final balance: ${alice.balance:.2f}")
    print(f"Bob final balance: ${bob.balance:.2f}")
    print(f"Charlie final balance: ${charlie.balance:.2f}")
