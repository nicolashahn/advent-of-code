square = 312051


def ring(x):
    # ring distance from starting point (1)
    radius = 0
    while x > (radius * 2 + 1)**2:
        radius += 1
    # lower right corner of the ring at this radius
    lr = (radius * 2 + 1)**2
    # count of how many steps we walk downwards along the spiral
    neg = 0
    # distance from the central axes (x or y) which intersect the center
    # of the spiral
    axis_dist = radius
    # are we walking away or towards an axis?
    direction = -1
    while lr - neg > x:
        neg += 1
        axis_dist += direction
        if axis_dist == radius or axis_dist == 0:
            direction *= -1
    return radius + axis_dist


print(ring(312051))
