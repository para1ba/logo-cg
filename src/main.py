from glumpy import app, gl, gloo
import utils

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(0.85 * position, 0.0, 1.0);
}
"""

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

window = app.Window(width=WIDTH, height=HEIGHT)

@window.event
def on_draw(dt):
    window.clear()
    circle3.draw(gl.GL_TRIANGLE_STRIP)
    circle1.draw(gl.GL_TRIANGLE_STRIP)
    star.draw(gl.GL_TRIANGLE_STRIP)
    triangles.draw(gl.GL_TRIANGLE_STRIP)
    circle2.draw(gl.GL_TRIANGLE_STRIP)

arr1 = utils.gen_dots_circle()
arr2 = utils.gen_dots_circle(y_move=-0.25, radius=0.75) 
arr3 = utils.gen_dots_circle(radius=1.005)

arr_star = [(0.15, 0.8), (0, 0.8), (0, 0.7), 
            (0, 0.9), (0, 0.7), (0.1, 0.6)]
arr_star_inverted = utils.invert_x_axis(arr_star)

details = [(0.385, 0.3), (0.0, 0.6), (0.4, 0.59), 
           (0.385, 0.3), (0.0, 0.6), (0.0, 0.3), 
           (0.4, 0.5), (0.45, 0.65), (-0.4, 0.3), 
           (0.3, 0.5), (0.35, 0.75), (-0.4, 0.3)]
details_inverted = utils.invert_x_axis(details)
#details_inverted = []

circle1 = gloo.Program(vertex, fragment_green, count=len(arr1))
circle1['position'] = arr1

#circle2 = gloo.Program(vertex, fragment_white, count=len(arr2))
circle2 = gloo.Program(vertex, fragment_green, count=len(arr2))
circle2['position'] = arr2

circle3 = gloo.Program(vertex, fragment_white, count=len(arr3))
circle3['position'] = arr3

star = gloo.Program(vertex, fragment_white, count=len(arr_star + arr_star_inverted))
star['position'] = arr_star + arr_star_inverted

triangles = gloo.Program(vertex, fragment_white, count=len(details + details_inverted))
triangles['position'] = details + details_inverted

app.run()