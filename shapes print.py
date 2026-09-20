import turtle
turtle.Screen().bgcolor("yellow")
turtle.Screen().setup(400,400)
polygon = turtle.Turtle()
num_sides = 6
side_lenth = 70
angle = 360.0 / num_sides

for i in range(num_sides):
    polygon.forward(side_lenth)
    polygon.right(angle)