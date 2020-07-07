import time
import io

from flask import Flask, Response
from matplotlib import pyplot
import numpy as np

from robot_imu import RobotImu



app = Flask(__name__)
imu = RobotImu()
samples_on_screen = 100
accel_list = []
sample_numbering = range(0, 100)


def make_accel_frame(accel_vector):
    """Generate an accelerometer frame - looks like this might be slow"""
    accel_list.append(accel_vector)
    if len(accel_list) >= samples_on_screen:
        accel_list.pop(0)

    fig = pyplot.figure()
    axes = pyplot.gca()
    axes.set_xlim(0, 100)
    axes.set_ylim(-2, 2)

    pyplot.plot(sample_numbering[:len(accel_list)], [v.x for v in accel_list], 'r')
    pyplot.plot(sample_numbering[:len(accel_list)], [v.y for v in accel_list], 'g')
    pyplot.plot(sample_numbering[:len(accel_list)], [v.z for v in accel_list], 'b')

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
        time.sleep(0.05)


@app.route('/')
def display():
    return Response(graph_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
