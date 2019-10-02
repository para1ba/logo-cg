from glumpy import app, gl, gloo
import utils
import math
import numpy as np

vertex = """
        uniform float scale;
        uniform float theta;
        uniform float dx;
        uniform float dy;
        attribute vec2 position;
        void main (void)
        {
            float ct = cos(theta);
            float st = sin(theta);
            float x = position.x * ct - position.y * st;
            float y = position.x * st + position.y * ct;
            gl_Position = vec4(0.85*(scale * x + dx), 0.85*(scale * y + dy), 0.0, 1.0);
        }
"""
            #gl_Position = vec4(0.85 * position, 0.0, 1.0);

fragment_green = """
        void main(void)
        {
            gl_FragColor = vec4(0.0, 0.396078, 0.231373,1.0);
        }
"""

fragment_white = """
        void main(void)
        {
            gl_FragColor = vec4(1.0, 1.0, 1.0,1.0);
        }
"""

WIDTH = 800
HEIGHT = 800
programs = []
lines = []
scale = 1.0
theta = 0.0
dx = 0.0
dy = 0.0
window = app.Window(width=WIDTH, height=HEIGHT)

@window.event
def on_draw(dt):
    global lines
    gl.glLineWidth(10)
    window.clear()
    for program in programs:
        program['theta'] = theta
        program['scale'] = scale
        program['dx'] = dx
        program['dy'] = dy
        #program.draw(gl.LINE_STRIP)
    
    #circle3.draw(gl.GL_TRIANGLE_STRIP)
    circle1.draw(gl.GL_TRIANGLE_STRIP)
    star.draw(gl.GL_TRIANGLE_STRIP)
    triangles.draw(gl.GL_TRIANGLE_STRIP)
    circle2.draw(gl.GL_TRIANGLE_STRIP)
    things.draw(gl.GL_TRIANGLE_STRIP)
    for line in lines:
        line.draw(gl.GL_LINE_STRIP)

@window.event
def on_key_press(symbol, modifiers):
    global scale
    global theta
    global dx
    global dy
    global mode
    if symbol == 45 and modifiers == 0:
        scale -= 0.1
    elif symbol == 61 and modifiers == 0:
        scale += 0.1
    elif symbol == 82:
        theta += 1.5 * math.pi / 180.0
    elif symbol == 69:
        theta -= 1.5 * math.pi / 180.0
    elif symbol == 87:
        dy += 0.1
    elif symbol == 65:
        dx -= 0.1
    elif symbol == 83:
        dy -= 0.1
    elif symbol == 68:
        dx += 0.1
    elif symbol == 32:
        scale = 1.0
        theta = 0.0
        dx = 0.0
        dy = 0.0

arr1 = utils.gen_dots_circle()
arr2 = utils.gen_dots_circle(y_move=-0.25, radius=0.75)
arr3 = utils.gen_dots_circle(radius=1.005)
arr4 = utils.gen_dots_circle(y_move=-0.25, radius=0.7)
arr5 = utils.gen_dots_circle(y_move=0.25, radius=0.25)

arr_star = [(0.15, 0.8), (0, 0.8), (0, 0.7), 
            (0, 0.9), (0, 0.7), (0.1, 0.6)]
arr_star_inverted = utils.invert_x_axis(arr_star)

details = [(0.385, 0.3), (0.0, 0.6), (0.4, 0.59), 
           (0.385, 0.3), (0.0, 0.6), (0.0, 0.3), 
           (0.4, 0.5), (0.45, 0.65), (-0.4, 0.3), 
           (0.3, 0.5), (0.35, 0.75), (-0.4, 0.3)]
details_inverted = utils.invert_x_axis(details)

circle1 = gloo.Program(vertex, fragment_green, count=len(arr1))
circle1['position'] = arr1

circle2 = gloo.Program(vertex, fragment_green, count=len(arr2))
circle2['position'] = arr2

circle3 = gloo.Program(vertex, fragment_white, count=len(arr3))
circle3['position'] = arr3

circle4 = gloo.Program(vertex, fragment_white, count=len(arr4))
circle4['position'] = arr4

circle5 = gloo.Program(vertex, fragment_white, count=len(arr5))
circle5['position'] = arr5

'''
fio = utils.curve4_bezier((0, 0.4), (-0.2, -0.2), (0.2, -0.5), (0, -0.9))
hair1 = gloo.Program(vertex, fragment_white, count=len(fio))
hair1['position'] = fio
'''

#curva2 = gloo.Program(vertex, fragment_white, count=len(up_points))
#curva2['position'] = up_points

star = gloo.Program(vertex, fragment_white, count=len(arr_star + arr_star_inverted))
star['position'] = arr_star + arr_star_inverted

triangles = gloo.Program(vertex, fragment_white, count=len(details + details_inverted))
triangles['position'] = details + details_inverted

programs.append(circle3)
programs.append(circle1)
programs.append(triangles)
programs.append(circle2)
programs.append(circle4)
programs.append(circle5)
programs.append(star)

dots = utils.gen_dots_circle(y_move=0.2, radius=0.25, modifier=0.8)
all_dots = dots + utils.invert_x_axis(dots)

dots = utils.gen_dots_circle(y_move=-0.4, radius=0.45, modifier=0.5)
all_dots = all_dots + dots + utils.invert_x_axis(dots)

dots = utils.gen_dots_circle(y_move=-0.8, radius=0.2, modifier=0.8)
all_dots = all_dots + dots + utils.invert_x_axis(dots)

things = gloo.Program(vertex, fragment_white, count=len(all_dots))
things['position'] = all_dots
programs.append(things)

hair, hair2 = utils.draw_my_form()
for fio in hair:
    line = gloo.Program(vertex, fragment_white, count=len(fio))
    line['position'] = fio
    lines.append(line)
    programs.append(line)
    line = gloo.Program(vertex, fragment_white, count=len(fio))
    line['position'] = utils.invert_x_axis(fio)
    lines.append(line)
    programs.append(line)
for fio in hair2:
    line = gloo.Program(vertex, fragment_green, count=len(fio))
    line['position'] = fio
    lines.append(line)
    programs.append(line)
    line = gloo.Program(vertex, fragment_green, count=len(fio))
    line['position'] = utils.invert_x_axis(fio)
    lines.append(line)
    programs.append(line)

for program in programs:
    program['scale'] = 1.0
    program['dx'] = 0.0
    program['dy'] = 0.0

app.run()
