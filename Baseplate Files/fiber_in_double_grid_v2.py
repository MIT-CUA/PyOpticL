from PyOpticL import layout, optomech
from fiber_input_splitter import fb_input_splitter
from test_doublepass import doublepass

# All x and y position inputs are in inches, not millimeters
# as defined in library

test_y=6.65/25.4

x1, y1 = 3,3
x2 = 5.75+3
y2 = 30.95/25.4-0.25-39/25.4+3+test_y
x3 = 5.75+3
y3 = 5.75+30.95/25.4-39/25.4+3+test_y


def ta_double_grid():
    layout.table_grid(dx=30, dy=17)
    fb_input_splitter(x=x1, y=y1, angle=0)
    doublepass(x=x2, y=y2, angle=0)
    doublepass(x=x3,y=y3,angle=0)

if __name__ == "__main__":
    ta_double_grid()
    layout.redraw()