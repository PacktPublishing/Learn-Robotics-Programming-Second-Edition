import vpython as vp


def make_robot():
    base = vp.box(size=vp.vector(155, 200, 3))
    wheel_thickness = 26
    wheel_dist = 155/2 # + wheel_thickness/2
    wheel_y = 20
    wheel_radius = 70/2
    wheel_l = vp.cylinder(radius=wheel_radius, length=wheel_thickness,
                          pos=vp.vector(-wheel_dist, wheel_y, 0), axis=vp.vector(1, 0, 0))
    wheel_r = vp.cylinder(radius=wheel_radius, length=wheel_thickness,
                          pos=vp.vector(wheel_dist, wheel_y, 0), axis=vp.vector(-1, 0, 0))
    return vp.compound([base, wheel_l, wheel_r])
