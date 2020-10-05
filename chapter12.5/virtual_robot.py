import vpython as vp
from robot_pose import robot_view


def make_robot():
    # length is along x axis.
    base = vp.box(length=200, height=3, width=155)
    # rotate to match body - so Z is height and Y is width
    base.rotate(angle=vp.radians(90),
                axis=vp.vector(1, 0, 0))
    wheel_thickness = 26
    wheel_dist = 155/2 # + wheel_thickness/2
    wheel_z = -20
    wheel_x = 30
    wheel_radius = 70/2
    wheel_l = vp.cylinder(radius=wheel_radius,
          length=wheel_thickness,
          pos=vp.vector(wheel_x, -wheel_dist, wheel_z),
          axis=vp.vector(0, -1, 0))
    wheel_r = vp.cylinder(radius=wheel_radius,
          length=wheel_thickness,
          pos=vp.vector(wheel_x, wheel_dist, wheel_z),
          axis=vp.vector(0, 1, 0))
    rear_castor = vp.cylinder(radius=14, length=12,
          pos=vp.vector(-80, -6, -30),
          axis=vp.vector(0, 1, 0))
    return vp.compound([base, wheel_l, wheel_r, rear_castor])


if __name__ == "__main__":
    robot_view()
    x_arrow = vp.arrow(axis=vp.vector(200, 0, 0), color=vp.color.red)
    y_arrow = vp.arrow(axis=vp.vector(0, 200, 0), color=vp.color.green)
    z_arrow = vp.arrow(axis=vp.vector(0, 0, 200), color=vp.color.blue)
    robot=make_robot()
    print(robot.up)
