from turtle import Turtle, done
from colorsys import hls_to_rgb

t = Turtle()

t.shape("turtle")
t.color("blue")
t.speed(0)


def draw_colored_hexagonal_spiral():
    colors = ["red", "green", "blue", "orange", "purple"]
    for i in range(36):
        t.color(colors[i % len(colors)])
        t.forward(i * 10)
        t.right(60)


def draw_colored_spiral():
    limit = 360
    for i in range(limit):
        r, g, b = hls_to_rgb(i / limit, 0.5, 0.5)
        t.color(r, g, b)
        t.forward(i * 0.1)
        t.right(10)

draw_colored_spiral()
#draw_colored_hexagonal_spiral()

done()
