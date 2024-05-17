import itertools
from datetime import datetime
from functools import wraps

# Custom exception for insufficient funds
class InsufficientFunds(Exception):
    """ Exception for when the buyer doesn't have enough funds to purchase a car. """
    def __init__(self, message):
        super().__init__(message)

# Decorator for transaction logging
def transaction_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            print(f"Transaction successful: {func.__name__} with args {args}, kwargs {kwargs}")
        else:
            print(f"Transaction failed: {func.__name__} with args {args}, kwargs {kwargs}")
        return result
    return wrapper

# Car class with auto-generated ID
class Car:
    _ids = itertools.count(1)

    def __init__(self, make, model, price):
        self.id = next(self._ids)
        self.__make = make
        self.__model = model
        self.__price = price

    @property
    def make(self):
        return self.__make

    @property
    def model(self):
        return self.__model

    @property
    def price(self):
        return self.__price

    def __str__(self):
        return f"{self.__make} {self.__model}, price: {self.__price} UAH."

# Car dealership class implementing an iterator and containing a list of cars
class Dealership:
    def __init__(self):
        self.__cars = []

    def add_car(self, car):
        self.__cars.append(car)

    @transaction_logger
    def sell_car(self, index, buyer):
        try:
            car = self.__cars[index]
            if buyer.balance >= car.price:
                buyer.decrease_balance(car.price)
                self.__cars.pop(index)
                return Contract(buyer, car)
            else:
                raise InsufficientFunds("You do not have enough funds to purchase this car.")
        except IndexError:
            raise IndexError("The selected car index is out of available options.")

    def __iter__(self):
        return iter(self.__cars)

    # Generator for filtering cars by a certain price
    def cars_by_price(self, min_price):
        for car in self.__cars:
            if car.price >= min_price:
                yield car

# Buyer class with auto-generated ID
class Buyer:
    _ids = itertools.count(1)

    def __init__(self, name, balance):
        self.id = next(self._ids)
        self.__name = name
        self.__balance = balance

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        self.__name = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value

    def decrease_balance(self, amount):
        if amount > self.__balance:
            raise InsufficientFunds("You do not have enough funds to purchase this car.")
        self.__balance -= amount

    def __str__(self):
        return f"Buyer {self.__name}, balance: {self.__balance} UAH."

# Contract class with auto-generated ID and date
class Contract:
    _ids = itertools.count(1)

    def __init__(self, buyer, car):
        self.id = next(self._ids)
        self.__buyer = buyer
        self.__car = car
        self.__date = datetime.now()

    def __str__(self):
        return f"Contract {self.id}: {self.__buyer.name} bought {self.__car} on {self.__date}"

# Testing and demonstration of the system
if __name__ == "__main__":
    dealership = Dealership()
    dealership.add_car(Car("Tesla", "Model S", 3000000))
    dealership.add_car(Car("Ford", "Fiesta", 500000))

    buyer = Buyer("Alexander", 2500000)

    print("Available cars:")
    for i, car in enumerate(dealership):
        print(f"{i}: {car}")

    while True:
        try:
            choice = int(input("Enter the number of the car you want to buy: "))
            contract = dealership.sell_car(choice, buyer)
            print(contract)
            break
        except ValueError:
            print("Please enter a valid car number.")
        except (InsufficientFunds, IndexError) as e:
            print(e)
            print("Please try again.")
