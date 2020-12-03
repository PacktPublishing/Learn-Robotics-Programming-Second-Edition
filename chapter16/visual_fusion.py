import vpython as vp
from robot_imu import RobotImu, ImuFusion
from delta_timer import DeltaTimer
import imu_settings
import virtual_robot

imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets,
               mag_offsets=imu_settings.mag_offsets)
fusion = ImuFusion(imu)

robot_view = vp.canvas(align="left")
model = virtual_robot.make_robot()
virtual_robot.robot_view()

compass = vp.canvas(width=400, height=400)
vp.cylinder(radius=1, axis=vp.vector(0, 0, 1), 
            pos=vp.vector(0, 0, -1))
needle = vp.arrow(axis=vp.vector(1, 0, 0), 
                  color=vp.color.red)


vp.graph(xmin=0, xmax=60, scroll=True)
graph_roll = vp.gcurve(color=vp.color.red)
graph_pitch = vp.gcurve(color=vp.color.green)
graph_yaw = vp.gcurve(color=vp.color.blue)

timer = DeltaTimer()

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    fusion.update(dt)
    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(fusion.roll), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(fusion.pitch), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(fusion.yaw), axis=vp.vector(0, 0, 1))
    needle.axis = vp.vector(
            vp.sin(vp.radians(fusion.yaw)), 
            vp.cos(vp.radians(fusion.yaw)), 
            0)
    graph_roll.plot(elapsed, fusion.roll)
    graph_pitch.plot(elapsed, fusion.pitch)
    graph_yaw.plot(elapsed, fusion.yaw)
