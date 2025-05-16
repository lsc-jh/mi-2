for i in range(1,11):
    for j in range(i):
        print(i,end=' ')
    print("")

# Task 2 - numbers from 1300 to 2100 that are divisible by 7 and multiple of 4
for i in range(1300,2101):
    if i % 7 == 0 and i % 4 == 0:
        print(i,end=' ')
print("")

# Task 3 - print all the possible names
first_name = ["Amy", "Jake", "Raymond", "Charles"]
last_name = ["Peralta", "Santiago", "Holt", "Boyle"]
for i in first_name:
    for j in last_name:
        print(i, j) # the same as print(i + " " + j)

# Task 4 - find all the pairs in the list
names = ["Martin", "Steven", "Quentin", "Alfred", "Tim", "Christopher", "James"]
for i in range(len(names)):
    for j in range(len(names)):
        if i < j:
            print(names[i] + " and " + names[j])

# Task 5 - Draw a triangle
import turtle

turtle_screen = turtle.getscreen()
turtle_actor = turtle.Turtle()
def shape1():
    turtle_actor.color('red')
    turtle_actor.fillcolor('yellow')
    turtle_actor.begin_fill()
    for i in range(3):
        turtle_actor.forward(100)
        turtle_actor.left(120)
    turtle_actor.end_fill()
    #turtle.exitonclick()

def shape2():
    # reset turtle
    color_list = ['red', 'yellow', 'blue', 'green', 'pink', 'orange', 'purple', 'brown']
    for i in range(3, 11):
        turtle_actor.color(color_list[10-i])
        turtle_actor.fillcolor(color_list[10-i])
        turtle_actor.begin_fill()
        for j in range(13-i):
            turtle_actor.forward(60)
            turtle_actor.left(360/(13-i))
        turtle_actor.end_fill()
    #turtle.exitonclick()

def shape3():
    for i in range(4):
        turtle_actor.forward(100)
        turtle_actor.left(90)
    turtle_actor.forward(10)
    turtle_actor.left(90)
    turtle_actor.forward(40)
    turtle_actor.right(90)
    turtle_actor.forward(25)
    turtle_actor.right(90)
    turtle_actor.forward(40)
    turtle_actor.left(90)

    turtle_actor.forward(65)
    turtle_actor.left(90)
    turtle_actor.forward(100)
    turtle_actor.left(45)
    turtle_actor.forward(70)
    turtle_actor.left(90)
    turtle_actor.forward(70.9)
    turtle_actor.left(135)
    turtle_actor.forward(100)
    turtle_actor.right(90)
    turtle_actor.forward(70.9)
    for i in range(10):
        turtle_actor.left(90)
        turtle_actor.forward(20)
        turtle_actor.right(90)
        turtle_actor.forward(30)
        turtle_actor.forward(-30)
    turtle_actor.penup()
    turtle_actor.setposition(20, 60)
    turtle_actor.setheading(0)
    for j in range(2):
        for i in range(4):
            turtle_actor.pendown()
            turtle_actor.forward(20)
            turtle_actor.left(90)
        turtle_actor.penup()
        turtle_actor.forward(40)

    #turtle.exitonclick()

#shape1()
shape2()
#shape3()

my_number = int(input("Give me a number: "))
prime_divisors = []
for i in range(1,my_number+1):
    if my_number % i == 0:
        prime_divisors.append(i)
if len(prime_divisors) > 2:
    print(str(my_number) + " is not a prime number because it has " + str(len(prime_divisors)) + " divisors. These divisors are:" + str(prime_divisors))
else:
    print(str(my_number) + " is a prime number because it has only " + str(len(prime_divisors)) + " divisors, one and itself.")

# Task 9 - rotating a list
list = [1,2,3,4,5,6]
print(list)
rotate = int(input("How much you want to rotate on the list?\n"))
rotate = rotate % 6
direction = input("In which direction do you want to rotate?(left/right)\n")
if direction == "left":
    list = list[rotate:] + list[:rotate]
else:
    list = list[-rotate:] + list[:-rotate]
print(list)


# Task 10
for i in range(12):
    for j in range(3):
        turtle_actor.forward(100)
        turtle_actor.left(120)
    turtle_actor.left(30)
turtle.exitonclick()

