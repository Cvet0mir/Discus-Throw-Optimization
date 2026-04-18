import math

def apply_throw(body, angle_deg, velocity, hand_pos):
    theta = math.radians(angle_deg)

    vx = velocity * math.cos(theta)
    vy = -velocity * math.sin(theta)

    body.velocity = (vx, vy)

