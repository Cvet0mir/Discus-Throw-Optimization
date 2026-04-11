import math

SCALE = 50
g = 9.81 * SCALE

def compute_trajectory(start_x, ground_y, angle_deg, velocity, height_cm):
    points = []

    theta = math.radians(angle_deg)

    v = velocity * SCALE

    vx = v * math.cos(theta)
    vy = -v * math.sin(theta)

    height_m = height_cm / 100
    start_y = ground_y - height_m * SCALE

    t = 0
    dt = 0.05

    while True:
        x = start_x + vx * t
        y = start_y + vy * t + 0.5 * g * t**2

        if y >= ground_y:
            return points, (x, ground_y)

        points.append((int(x), int(y)))
        t += dt

