import vpython as vp


def make_robot():
    base = vp.box(length=200, height=3, width=200)
    wheel_thickness = 26
    wheel_dist = 155/2 # + wheel_thickness/2
    wheel_y = -20
    wheel_z = 30
    wheel_radius = 70/2
    wheel_l = vp.cylinder(radius=wheel_radius, length=wheel_thickness,
                          pos=vp.vector(-wheel_dist, wheel_y, wheel_z), axis=vp.vector(-1, 0, 0))
    wheel_r = vp.cylinder(radius=wheel_radius, length=wheel_thickness,
                          pos=vp.vector(wheel_dist, wheel_y, wheel_z), axis=vp.vector(1, 0, 0))
    rear_castor = vp.cylinder(radius=14, length=12, pos=vp.vector(0, -30, -80))
    return vp.compound([base, wheel_l, wheel_r, rear_castor])


if __name__ == "__main__":
    make_robot()
