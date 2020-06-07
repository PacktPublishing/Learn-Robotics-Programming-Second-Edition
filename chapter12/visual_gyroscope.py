import time
import io
import math
from robot_imu import RobotImu, Vector3

from flask import Flask, Response
from matplotlib import pyplot as plt, patches


app = Flask(__name__)
imu = RobotImu()


crosshair_width = 0.01
crosshair_height = 0.1


class GyroAccumulator(Vector3):
    def __add__(self, other):
        return GyroAccumulator(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)


gyro_cumulative = GyroAccumulator(0, 0, 0)


def make_gyro_ball(gyro_vector):
    global gyro_cumulative
    gyro_cumulative += gyro_vector
    z_rad = math.radians(gyro_cumulative.z)
    x_angle_mod = gyro_cumulative.x / 180
    y_angle_mod = gyro_cumulative.y / 180

    ax = plt.subplot()
    axes = plt.gca()
    axes.set_xlim(-1, 1)
    axes.set_ylim(-1, 1)

    clip_path = patches.Ellipse((0, 0,), 2, 2, 0)
    gyro_patches = [
        patches.Rectangle((-1, -1), 2, 2, 0, color='xkcd:blue'),
        patches.Wedge((0, x_angle_mod), 2, 180 + gyro_cumulative.z, 0 + gyro_cumulative.z, color='xkcd:brown'),
        patches.Wedge(
            (0 + math.cos(z_rad) * y_angle_mod, x_angle_mod + math.sin(z_rad) * y_angle_mod),
            0.1, 80 + gyro_cumulative.z, 100 + gyro_cumulative.z, color='xkcd:green'
        )
    ]
    ax.add_patch(clip_path)
    [patch.set_clip_path(clip_path) for patch in gyro_patches]
    [ax.add_patch(patch) for patch in gyro_patches]

    # crosshair
    ax.add_patch(
        patches.Rectangle((-crosshair_width, 0.25 - crosshair_height), 2 * crosshair_width, crosshair_height, 0,
                          color='xkcd:white'))
    ax.add_patch(
        patches.Rectangle((-crosshair_width, -0.25), 2 * crosshair_width, crosshair_height, 0, color='xkcd:white'))

    ax.add_patch(
        patches.Rectangle((0.25 - crosshair_height, -crosshair_width), crosshair_height, 2 * crosshair_width, 0,
                          color='xkcd:white'))
    ax.add_patch(
        patches.Rectangle((-0.25, -crosshair_width), crosshair_height, 2 * crosshair_width, 0, color='xkcd:white'))


def make_gyro_meter(color, title, degrees_per_second, index):
    plt.subplot(1, 3, index, projection="polar")
    axes = plt.gca()
    axes.get_yaxis().set_ticklabels([])
    axis = [math.radians(degrees_per_second)]
    plt.polar(axis, [1], '{}o'.format(color))
    plt.title(title, loc='left')


def make_gyro_frame(gyro_vector):
    """Generate an accelerometer frame"""
    fig = plt.figure()
    make_gyro_ball(gyro_vector)
    # make_gyro_meter('r', 'x', gyro_vector.x, 1)
    # make_gyro_meter('g', 'y', gyro_vector.y, 2)
    # make_gyro_meter('b', 'z', gyro_vector.z, 3)
    output = io.BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    return output.getvalue()


def graph_generator():
    """Graph output as video feed"""
    while True:
        # get sample data
        output = make_gyro_frame(imu.read_gyro())
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + output + b'\r\n')
        time.sleep(0.01)


@app.route('/')
def display():
    return Response(graph_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
