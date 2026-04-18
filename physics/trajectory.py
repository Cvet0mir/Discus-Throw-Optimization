import math

SCALE = 50
g = 9.81 * SCALE

def compute_trajectory(start_x, start_y, angle_deg, velocity):
    points = []

    theta = math.radians(angle_deg)

    v = velocity * SCALE

    vx = v * math.cos(theta)
    vy = -v * math.sin(theta)

    t = 0
    dt = 0.05

    while True:
        x = start_x + vx * t
        y = start_y + vy * t + 0.5 * g * t**2

        if y >= 600:
            return points, (x, 600)

        points.append((int(x), int(y)))
        t += dt

