import math


def generate_trajectory_with_step(x1, y1, x2, y2, step_size):
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance == 0:
        return [(x1, y1)]

    steps = math.ceil(distance / step_size)

    if dy == 0:
        step_dx = step_size if dx > 0 else -step_size
        step_dy = 0
    elif dx == 0:
        step_dx = 0
        step_dy = step_size if dy > 0 else -step_size
    else:
        step_dx = dx / steps
        step_dy = dy / steps

    trajectory = []
    for i in range(steps):
        new_x = x1 + step_dx * i
        new_y = y1 + step_dy * i
        trajectory.append((round(new_x), round(new_y)))

    trajectory.append((x2, y2))

    return trajectory
