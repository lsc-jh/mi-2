
class Car:
    def __init__(self, model, wheel_count, wheel_pressure):
        print(f"{model} is being built.")
        self.model = model
        self.wheel_count = wheel_count
        self.wheel_pressure = wheel_pressure

print("blueprint", Car)

car = Car("Mazda", 4, 2.4)
print(car.model, car)

toyota = Car("Toyota", 4, 2.2)
print(toyota.model, toyota)

