from glumpy import app, gl, gloo
import math

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(0.85*position, 0.0, 1.0);
}
"""

fragment = """
// Union (A or B)
  float csg_union(float d1, float d2)
  {
      return min(d1,d2);
  }
  // Intersection (A and B)
  float csg_intersection(float d1, float d2)
  {
      return max(d1,d2);
  }
  // Difference (A not B)
  float csg_difference(float d1, float d2)
  {
      return max(d1,-d2);
  }
  // Exclusion (A xor B)
  float csg_exclusion(float d1, float d2) 
  { 
     return -max(-max(d1, -max(d1,d2)), -max(d2, -max(d1,d2)));
  }
  // Signed distance to a circle
  float circle(vec2 p, vec2 center, float radius)
  {
      float d = length(p-center) - radius;
      return d;
  }
  vec4 color(float d)
  {
      vec3 white = vec3(1.0, 1.0, 1.0);
      vec3 blue  = vec3(0.1, 0.4, 0.7);
      vec3 color = white - sign(d)*blue;
      color *= (1.0 - exp(-4.0*abs(d))) * (0.8 + 0.2*cos(140.0*d));
      color = mix(color, white, 1.0-smoothstep(0.0,0.02,abs(d)) );
      return vec4(color, 1.0);
  
  }

    void main(void)
    {
        vec2 p = gl_FragCoord.xy;
        float d1 = circle(p, vec2(256.0-64.0, 256.0), 128.0);
        float d2 = circle(p, vec2(256.0+64.0, 256.0), 128.0);
        // float d = csg_exclusion(d1,d2);
        float d = csg_union(d1,d2);
        gl_FragColor = color(-d/128.0);
    }
"""

window = app.Window(width=800, height=600)

def drawCircle(num):
    glBegin(GL_LINE_LOOP)
    pi = math.pi
    for i in range(100):
        angle = 2*pi*i/100
        glVertex2f(math.cos(angle), math.sin(angle))
    glEnd()

@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

quad = gloo.Program(vertex, fragment, count=3)
quad['position'] = [(-1,-1), (-1,+1), (+1,-1)]
app.run()
