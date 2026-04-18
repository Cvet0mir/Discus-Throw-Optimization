import math

MAX_VELOCITY = 32
MIN_VELOCITY = 8

def clamp(value, min_v, max_v):
    return max(min_v, min(value, max_v))


def apply_throw(body, angle_deg, velocity, hand_pos):
    theta = math.radians(angle_deg)
    velocity = clamp(velocity, MIN_VELOCITY, MAX_VELOCITY)

    vx = velocity * math.cos(theta)
    vy = -velocity * math.sin(theta)

    body.velocity = (vx, vy)

