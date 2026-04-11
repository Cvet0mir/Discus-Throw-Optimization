import math

def apply_throw(body, angle_deg, velocity, height_cm, screen_height):
    theta = math.radians(angle_deg)

    vx = velocity * math.cos(theta)
    vy = -velocity * math.sin(theta)

    body.velocity = (vx, vy)
    height_px = height_cm

    x = body.position.x
    y = screen_height - height_px

    body.position = (x, y)
