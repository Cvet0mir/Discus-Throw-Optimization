import pymunk

def create_space():
    space = pymunk.Space()
    space.gravity = (0, 0)
    return space


def create_player(space):
    mass = 1
    radius = 20
    moment = pymunk.moment_for_circle(mass, 0, radius)

    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (150, 600)

    shape = pymunk.Circle(body, radius)
    space.add(body, shape)

    return body


def create_ground(space, width):
    ground = pymunk.Segment(space.static_body, (0, 600), (width, 600), 5)
    ground.friction = 1.0
    space.add(ground)


def apply_input(body, keys):
    if keys[0]:
        body.position = (body.position.x - 2, body.position.y)
    if keys[1]:
        body.position = (body.position.x + 2, body.position.y)


def step(space, dt):
    space.step(dt)

