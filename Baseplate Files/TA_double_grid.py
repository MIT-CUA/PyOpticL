from PyOpticL import layout, optomech
from TA_input_splitter import ta_input_splitter
from modular_doublepass_aom_updated import doublepass


x1, y1 = 0,0
x2 = 5.75
y2 = 30.95/25.4
x3 = 5.75
y3 = 5.75+30.95/25.4


def ta_double_grid():
    layout.table_grid(dx=30, dy=17)
    ta_input_splitter(x=x1, y=y1, angle=0)
    doublepass(x=x2, y=y2, angle=0)
    doublepass(x=x3,y=y3,angle=0)

if __name__ == "__main__":
    ta_double_grid()
    layout.redraw()