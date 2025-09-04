import turtle

def draw_fractal_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    if depth > 0:      
        length = length / 3
        draw_fractal_edge(length, depth - 1)
        turtle.right(60)       
        draw_fractal_edge(length, depth - 1)
        turtle.left(120)     
        draw_fractal_edge(length, depth - 1)
        turtle.right(60)
        draw_fractal_edge(length, depth - 1)

def draw_polygon(sides, length, depth):
    for i in range(sides):
        draw_fractal_edge(length, depth)
        turtle.right(360/ sides)

sides = int(input("Enter the number of sides: "))
length = int(input("Enter the side length: "))
depth = int(input("Enter the recursion depth: "))

draw_polygon(sides, length, depth)

turtle.done()
