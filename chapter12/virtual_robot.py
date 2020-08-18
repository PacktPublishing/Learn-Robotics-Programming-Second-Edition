import vpython as vp


def make_robot():
    base = vp.box(length=200, height=3, width=155)
    wheel_thickness = 26
    wheel_dist = 155/2 # + wheel_thickness/2
    wheel_y = -20
    wheel_x = 30
    wheel_radius = 70/2
    wheel_l = vp.cylinder(radius=wheel_radius,
          length=wheel_thickness,
          pos=vp.vector(wheel_x, wheel_y, -wheel_dist),
          axis=vp.vector(0, 0, -1))
    wheel_r = vp.cylinder(radius=wheel_radius,
          length=wheel_thickness,
          pos=vp.vector(wheel_x, wheel_y,  wheel_dist),
          axis=vp.vector(0, 0, 1))
    rear_castor = vp.cylinder(radius=14, length=12,
          pos=vp.vector(-80, -30, -7),
          axis=vp.vector(0, 0, 1))
    return vp.compound([base, wheel_l, wheel_r, rear_castor])


if __name__ == "__main__":
    make_robot()
