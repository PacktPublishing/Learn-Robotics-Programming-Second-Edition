import time
import io
from robot_imu import RobotImu

from flask import Flask, Response
from matplotlib import pyplot


app = Flask(__name__)
imu = RobotImu()


def make_accel_frame(accel_vector):
    """Generate an accelerometer frame"""
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    axes = pyplot.gca()
    axes.set_xlim(-1, 1)
    axes.set_ylim(-1, 1)
    axes.set_zlim(-1, 1)
    ax.plot([0.0, accel_vector[0]], [0.0, accel_vector[1]], [0.0, -accel_vector[2]], 'b-o')
    output = io.BytesIO()
    pyplot.savefig(output, format='png')
    pyplot.close(fig)
    return output.getvalue()


def graph_generator():
    """Graph output as video feed"""
    while True:
        # get sample data
        output = make_accel_frame(imu.read_accelerometer())
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + output + b'\r\n')
        time.sleep(0.1)


@app.route('/')
def display():
    return Response(graph_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
