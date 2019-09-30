import math

def circle_equation(radius=1.0):
    arr = []
    
    for x in range(math.ceil(radius*100)):
        arr.append((x/100, math.sqrt(abs(radius**2 - ((x/100)**2)))))
    
    return arr

def gen_dots_circle(x_move=0.0, y_move=0.0, radius=1.0):
    #arr = circle_equation(x_move, y_move, radius)
    arr = circle_equation(radius)
    resp = []
    zero_dot = (0, 0)
    for i in range(len(arr)-1):
        dot = arr[i]
        dot_aux = arr[i+1]
        p1 = (dot[0] + x_move, dot[1] + y_move)
        p1_aux = (dot_aux[0] + x_move, dot_aux[1] + y_move)
        resp.append(p1)
        resp.append(zero_dot)
        resp.append(p1_aux)
        p2 = (dot[0] + x_move, -dot[1] + y_move)
        p2_aux = (dot_aux[0] + x_move, -dot_aux[1] + y_move)
        resp.append(p2)
        resp.append(zero_dot)
        resp.append(p2_aux)
        p3 = (-dot[0] + x_move, dot[1] + y_move)
        p3_aux = (-dot_aux[0] + x_move, dot_aux[1] + y_move)
        resp.append(p3)
        resp.append(zero_dot)
        resp.append(p3_aux)
        p4 = (-dot[0] + x_move, -dot[1] + y_move)
        p4_aux = (-dot_aux[0] + x_move, -dot_aux[1] + y_move)
        resp.append(p4)
        resp.append(zero_dot)
        resp.append(p4_aux)
    dot = arr[-1]
    dot_aux = (radius, 0)
    p1 = (dot[0] + x_move, dot[1] + y_move)
    p1_aux = (dot_aux[0] + x_move, dot_aux[1] + y_move)
    resp.append(p1)
    resp.append(zero_dot)
    resp.append(p1_aux)
    p2 = (dot[0] + x_move, -dot[1] + y_move)
    p2_aux = (dot_aux[0] + x_move, -dot_aux[1] + y_move)
    resp.append(p2)
    resp.append(zero_dot)
    resp.append(p2_aux)
    p3 = (-dot[0] + x_move, dot[1] + y_move)
    p3_aux = (-dot_aux[0] + x_move, dot_aux[1] + y_move)
    resp.append(p3)
    resp.append(zero_dot)
    resp.append(p3_aux)
    p4 = (-dot[0] + x_move, -dot[1] + y_move)
    p4_aux = (-dot_aux[0] + x_move, -dot_aux[1] + y_move)
    resp.append(p4)
    resp.append(zero_dot)
    resp.append(p4_aux)
    
    return resp

def invert_x_axis(arr):
    resp = []
    
    for obj in arr:
        if obj[0] == 0:
            resp.append((obj[0], obj[1]))
        else:
            resp.append((-obj[0], obj[1]))
    
    return resp

def translate_dot(x, y):
    new_x = 2*x/WIDTH
    new_y = 2*y/HEIGHT
    return new_x, new_y

def made_square(arr):
    first_triangle = arr[0:3]
    second_triangle = arr[2:4]
    second_triangle.append(arr[0])
    return first_triangle + second_triangle