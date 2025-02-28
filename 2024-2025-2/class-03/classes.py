
class Car:
    created_cars = 0

    def __init__(self, model, wheel_count, wheel_pressure):
        print(f"{model} is being built.")
        Car.created_cars+=1
        self.model = model
        self.wheel_count = wheel_count
        self.wheel_pressure = wheel_pressure

    def __str__(self):
        return f"Model: {self.model}\nW.C.: {self.wheel_count}\nW.P.: {self.wheel_pressure}"

    def start(self):
        print(f"{self.model} says wrooom wrooom")

print("blueprint", Car)
print("created_cars", Car.created_cars)

car = Car("Mazda", 4, 2.4)
print(car.model, car)
car.start()

toyota = Car("Toyota", 4, 2.2)
print(toyota.model, toyota)
toyota.start()

cars = []
n = int(input("How many cars do you have? n = "))
for _ in range(n):
    _model = input("Model: ")
    _wheel_count = int(input("Wheel count: ") or 4)
    _wheel_pressure = float(input("Wheel pressure: ") or 2.2)
    cars.append(Car(_model, _wheel_count, _wheel_pressure))

for car in cars:
    print("--------------")
    print(car)
    print("--------------")


print("created cars", Car.created_cars)

