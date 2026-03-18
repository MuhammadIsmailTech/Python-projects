class Account:
    def __init__(self, account_number, name, balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. Remaining balance: {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient balance.")

    def display(self):
        print(f"\nAccount Number: {self.account_number}")
        print(f"Account Holder: {self.name}")
        print(f"Balance: {self.balance}\n")

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        acc_no = input("Enter account number: ")
        name = input("Enter account holder name: ")
        if acc_no in self.accounts:
            print("Account already exists.")
            return
        account = Account(acc_no, name)
        self.accounts[acc_no] = account
        print("Account created successfully!")

    def deposit_money(self):
        acc_no = input("Enter account number: ")
        if acc_no in self.accounts:
            amount = float(input("Enter amount to deposit: "))
            self.accounts[acc_no].deposit(amount)
        else:
            print("Account not found.")

    def withdraw_money(self):
        acc_no = input("Enter account number: ")
        if acc_no in self.accounts:
            amount = float(input("Enter amount to withdraw: "))
            self.accounts[acc_no].withdraw(amount)
        else:
            print("Account not found.")

    def check_balance(self):
        acc_no = input("Enter account number: ")
        if acc_no in self.accounts:
            self.accounts[acc_no].display()
        else:
            print("Account not found.")

    def menu(self):
        while True:
            print("\n--- Bank Management System ---")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.deposit_money()
            elif choice == '3':
                self.withdraw_money()
            elif choice == '4':
                self.check_balance()
            elif choice == '5':
                print("Thank you for using our bank system!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    bank = BankSystem()
    bank.menu()
