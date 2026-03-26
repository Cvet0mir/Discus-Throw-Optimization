import pymunk

def create_space():
    space = pymunk.Space()
    space.gravity = (0, 900)
    return space


def create_player(space):
    mass = 1
    radius = 20
    moment = pymunk.moment_for_circle(mass, 0, radius)

    body = pymunk.Body(mass, moment)
    body.position = (85, 475)

    shape = pymunk.Circle(body, radius)
    space.add(body, shape)

    return body


def create_ground(space, width):
    ground = pymunk.Segment(space.static_body, (0, 600), (width, 600), 5)
    ground.friction = 1.0
    space.add(ground)


def move_player(body, keys):
    if keys[True]:
        ...


def apply_input(body, keys):
    if keys[0]:
        body.apply_force_at_local_point((-2000, 0))
    if keys[1]:
        body.apply_force_at_local_point((2000, 0))


def step(space, dt):
    space.step(dt)


