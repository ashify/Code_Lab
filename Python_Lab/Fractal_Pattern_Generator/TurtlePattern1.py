import turtle


def draw_shape(a_turtle, size, sides):
    
    a_turtle.begin_fill()
    a_turtle.down()
    
    for i in range(sides):
        a_turtle.forward(size)
        a_turtle.right(360/sides)
        
    a_turtle.up()
    a_turtle.end_fill()

    
def draw_fractal():
    
    window = turtle.Screen()
    window.bgcolor("#B0E0E6")

    #Play with these variables to get different patterns!
    starting_coordinates = (150,-180)
    starting_angle= 180
    sides = 5
    length = 20
    turns = 5
    spacing_multiplier = 2
    shape_shrink_factor = 2

    #create turtle and set it's properties
    ash = turtle.Turtle()
    ash.shape("turtle")
    ash.color("plum")
    ash.speed(10)
    ash.penup()
    ash.goto(starting_coordinates)
    ash.pendown()

    #And the turtle starts drawing!
    ash.right(starting_angle)
    for i in range(sides):
        for i in range(sides):
            for i in range(sides):
                for i in range(sides):
                    draw_shape(ash, length/shape_shrink_factor, sides)
                    ash.forward(length*spacing_multiplier)
                    ash.right(360/turns)
                ash.forward(length*spacing_multiplier**2)
                ash.right(360/turns)
            ash.forward(length*spacing_multiplier**3)
            ash.right(360/turns)
        ash.forward(length*spacing_multiplier**4)
        ash.right(360/turns)
    window.exitonclick()

   
def main():
    draw_fractal()


if __name__ == "__main__":
    main()




