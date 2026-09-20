import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")  # Sets the background color

# Create a turtle object for drawing
my_turtle = turtle.Turtle()
my_turtle.shape("turtle")  # Changes the cursor shape to a turtle
my_turtle.color("blue")    # Sets the line color to blue
my_turtle.speed(2)         # Sets drawing speed (1=slow, 10=fast)

# Loop 4 times to draw each side of the square
for _ in range(4):
    my_turtle.forward(100) # Move forward by 100 pixels
    my_turtle.left(90)     # Turn left by 90 degrees

# Keep the window open until you click on it
screen.exitonclick()
