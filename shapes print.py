import turtle
turtle.Screen().bgcolor("turquoise")
turtle.Screen().setup(480,4000)
polygon = turtle.Turtle()
num_sides = 6
side_lenth = 70
angle = 356.09 / num_sides

for i in range(num_sides):
    polygon.forward(side_lenth)
    polygon.left(angle)