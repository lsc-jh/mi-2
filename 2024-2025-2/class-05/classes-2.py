class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def drive(self):
        print(f"The {self.color} {self.brand} is driving.")


class ElectricCar(Car):
    def __init__(self, brand, color, battery):
        super().__init__(brand, color)
        self.battery = battery

    def charge(self):
        print(f"The {self.color} {self.brand} is charging its {self.battery} battery.")


opel = Car("Opel", "green")
opel.drive()

tesla = ElectricCar("Tesla", "blue", "100kWh")
tesla.drive()
tesla.charge()
