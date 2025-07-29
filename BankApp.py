from datetime import date, timedelta, datetime

class User:

    user_counter = 1

    def __init__(self, name, surname, account_list=None):
        self.name = name
        self.surname = surname
        self.id = User.user_counter
        User.user_counter += 1
        self.account_list = account_list if account_list is not None else []

    def add_account(self, account):
        if len(self.account_list) < 2:
            self.account_list.append(account)
        else:
            print("This user already has 2 accounts.")

    def __str__(self):
        return f"User {self.name} {self.surname} (ID: {self.id}) - Accounts: {len(self.account_list)}"


class Account:

    acCounter = 100

    def __init__(self, balance, acType):
        self.acId = Account.acCounter
        Account.acCounter += 5
        self.balance = balance
        self.acType = acType.lower()

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposit amount: {amount} New balance: {self.balance}")
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdraw amount: {amount} New balance: {self.balance}")
            return True
        else:
            print("You don't have enough money.")
            return False


class CurrentAccount(Account):
    def __init__(self, balance):
        super().__init__(balance, "current")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"✅ {amount}₺ successfully deposited.")
            print(f"📌 New balance: {self.balance:.2f}₺")
        else:
            print("❌ Invalid amount. Please enter a positive value.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"✅ {amount}₺ successfully withdrawn.")
            print(f"📌 Remaining balance: {self.balance:.2f}₺")
            return True
        else:
            print("❌ Insufficient balance or invalid amount.")
            return False


class TermAccount(Account):
    def __init__(self, balance):
        super().__init__(balance, "Term")
        self.interest_rate = 0.20  # 20% interest
        self.maturity_days = 90
        self.opening_date = datetime.now()
        self.interest_applied = False

    def withdraw(self, amount):
        print("❌ Withdrawals from a term account are not allowed before the maturity period ends.")
        return False

    def calculate_interest(self):
        today = datetime.now()
        days_passed = (today - self.opening_date).days

        if days_passed >= self.maturity_days:
            if not self.interest_applied:
                interest = self.balance * self.interest_rate * self.maturity_days / 365
                print(f"✔️ Interest earned after {self.maturity_days} days: {interest:.2f}₺")
                self.balance += interest
                self.interest_applied = True
                print(f"Interest applied: {interest:.2f}\n Current balance: {self.balance}")
                return interest
            else:
                print("Interest already applied. Cannot apply again.")
                return 0
        else:
            print(
                f"⏳ Maturity period has not yet been reached ({days_passed}/{self.maturity_days} days passed). No interest earned.")
            return 0


class Bank:
    def __init__(self):
        self.customers = []

    def add_customer(self, name, surname):
        user = User(name, surname)
        self.customers.append(user)
        print(f"Customer added: {name} {surname}")
        return user

    def list_customers(self):
        for user in self.customers:
            print(user)

    def find_customer(self, user_id):
        for user in self.customers:
            if user.id == user_id:
                return user
        print("Customer not found")
        return None

    def create_account(self, user_id, ac_type, balance):
        user = self.find_customer(user_id)
        if user:
            if ac_type == "current":
                account = CurrentAccount(balance)
            elif ac_type == "term":
                account = TermAccount(balance)
            else:
                print("Invalid account type.")
                return

            user.add_account(account)
            print(f"{ac_type.capitalize()} account added. Account No: {account.acId}")

    def transfer(self, from_account, to_account, amount):
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            print(f"{amount}₺ successfully transferred to account ID {to_account.acId}")
        else:
            print("Transfer Failed. Balance is not enough.")
