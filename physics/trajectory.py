import math

g = 9.81

def compute_trajectory(start_x, start_y, angle_deg, velocity, ppm):
    points = []

    theta = math.radians(angle_deg)

    velocity = max(8, min(32, velocity))

    v_pixels = velocity * ppm * 0.83

    vx = v_pixels * math.cos(theta)
    vy = -v_pixels * math.sin(theta)

    t = 0
    dt = 0.05

    while True:
        x = start_x + vx * t
        y = start_y + vy * t + 0.5 * g * ppm * t**2

        if y >= 600:
            return points, (x, 600)

        points.append((int(x), int(y)))
        t += dt

