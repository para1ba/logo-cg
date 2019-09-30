import math
import numpy as np


curve_distance_epsilon        = 1e-30
curve_collinearity_epsilon    = 1e-30
curve_angle_tolerance_epsilon = 0.01
curve_recursion_limit         = 32
m_cusp_limit                  = 0.0
m_angle_tolerance             = 10*math.pi/180.0
m_approximation_scale         = 1.0
m_distance_tolerance_square   = (0.5 / m_approximation_scale)**2

def curve4_bezier( p1, p2, p3, p4 ):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    points = []
    curve4_recursive_bezier( points, x1,y1, x2,y2, x3,y3, x4,y4 )

    dx,dy = points[0][0]-x1, points[0][1]-y1
    if (dx*dx+dy*dy) > 1e-10: points.insert(0, (x1,y1) )
    dx,dy = points[-1][0]-x4, points[-1][1]-y4
    if (dx*dx+dy*dy) > 1e-10: points.append( (x4,y4) )

    return np.array( points ).reshape(len(points),2)

def curve4_recursive_bezier( points, x1, y1, x2, y2, x3, y3, x4, y4, level=0):
    if level > curve_recursion_limit: 
        return

    # Calculate all the mid-points of the line segments
    # -------------------------------------------------
    x12   = (x1 + x2) / 2.
    y12   = (y1 + y2) / 2.
    x23   = (x2 + x3) / 2.
    y23   = (y2 + y3) / 2.
    x34   = (x3 + x4) / 2.
    y34   = (y3 + y4) / 2.
    x123  = (x12 + x23) / 2.
    y123  = (y12 + y23) / 2.
    x234  = (x23 + x34) / 2.
    y234  = (y23 + y34) / 2.
    x1234 = (x123 + x234) / 2.
    y1234 = (y123 + y234) / 2.


    # Try to approximate the full cubic curve by a single straight line
    # -----------------------------------------------------------------
    dx = x4 - x1
    dy = y4 - y1
    d2 = math.fabs(((x2 - x4) * dy - (y2 - y4) * dx))
    d3 = math.fabs(((x3 - x4) * dy - (y3 - y4) * dx))

    s =  int((d2 > curve_collinearity_epsilon) << 1) + int(d3 > curve_collinearity_epsilon)

    if s == 0:
        # All collinear OR p1==p4
        # ----------------------
        k = dx*dx + dy*dy
        if k == 0:
            d2 = calc_sq_distance(x1, y1, x2, y2)
            d3 = calc_sq_distance(x4, y4, x3, y3)

        else:
            k   = 1. / k
            da1 = x2 - x1
            da2 = y2 - y1
            d2  = k * (da1*dx + da2*dy)
            da1 = x3 - x1
            da2 = y3 - y1
            d3  = k * (da1*dx + da2*dy)
            if d2 > 0 and d2 < 1 and d3 > 0 and d3 < 1:
                # Simple collinear case, 1---2---3---4
                # We can leave just two endpoints
                return
             
            if d2 <= 0:
                d2 = calc_sq_distance(x2, y2, x1, y1)
            elif d2 >= 1:
                d2 = calc_sq_distance(x2, y2, x4, y4)
            else:
                d2 = calc_sq_distance(x2, y2, x1 + d2*dx, y1 + d2*dy)

            if d3 <= 0:
                d3 = calc_sq_distance(x3, y3, x1, y1)
            elif d3 >= 1:
                d3 = calc_sq_distance(x3, y3, x4, y4)
            else:
                d3 = calc_sq_distance(x3, y3, x1 + d3*dx, y1 + d3*dy)

        if d2 > d3:
            if d2 < m_distance_tolerance_square:
                points.append( (x2, y2) )
                return
        else:
            if d3 < m_distance_tolerance_square:
                points.append( (x3, y3) )
                return

    elif s == 1:
        # p1,p2,p4 are collinear, p3 is significant
        # -----------------------------------------
        if d3 * d3 <= m_distance_tolerance_square * (dx*dx + dy*dy):
            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append((x23, y23) )
                return
            
            # Angle Condition
            # ---------------
            da1 = math.fabs(math.atan2(y4 - y3, x4 - x3) - math.atan2(y3 - y2, x3 - x2))
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            
            if da1 < m_angle_tolerance:
                points.extend( [(x2, y2),(x3, y3)] )
                return

            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x3, y3) )
                    return

    elif s == 2:
        # p1,p3,p4 are collinear, p2 is significant
        # -----------------------------------------
        if d2 * d2 <= m_distance_tolerance_square * (dx*dx + dy*dy):
            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append( (x23, y23) )
                return
            
            # Angle Condition
            # ---------------
            da1 = math.fabs(math.atan2(y3 - y2, x3 - x2) - math.atan2(y2 - y1, x2 - x1))
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            
            if da1 < m_angle_tolerance:
                points.extend( [(x2, y2),(x3, y3)] )
                return
            
            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x2, y2) )
                    return
        
    elif s == 3:
        # Regular case
        # ------------
        if (d2 + d3)*(d2 + d3) <= m_distance_tolerance_square * (dx*dx + dy*dy):
            # If the curvature doesn't exceed the distance_tolerance value
            # we tend to finish subdivisions.

            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append( (x23, y23) )
                return
            
            # Angle & Cusp Condition
            # ----------------------
            k   = math.atan2(y3 - y2, x3 - x2)
            da1 = math.fabs(k - math.atan2(y2 - y1, x2 - x1))
            da2 = math.fabs(math.atan2(y4 - y3, x4 - x3) - k)
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            if da2 >= math.pi:
                da2 = 2*math.pi - da2

            if da1 + da2 < m_angle_tolerance:
                # Finally we can stop the recursion
                # ---------------------------------
                points.append( (x23, y23) )
                return
            
            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x2, y2) )
                    return
                
                if da2 > m_cusp_limit:
                    points.append( (x3, y3) )
                    return
    
    # Continue subdivision
    # --------------------
    curve4_recursive_bezier( points, x1, y1, x12, y12, x123, y123, x1234, y1234, level + 1 )
    curve4_recursive_bezier( points, x1234, y1234, x234, y234, x34, y34, x4, y4, level + 1 )

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
