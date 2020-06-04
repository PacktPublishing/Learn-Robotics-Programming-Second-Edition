import time
import io
from robot_imu import RobotImu

from flask import Flask, Response
from matplotlib import pyplot


app = Flask(__name__)
imu = RobotImu()


def make_thermometer_frame(temperature):
    """Generate a thermometer frame"""
    fig = pyplot.figure()
    pyplot.gca().set_ylim(10, 40)
    # plot as a red square
    pyplot.plot([temperature], 'rs')

    output = io.BytesIO()
    pyplot.savefig(output, format='png')
    pyplot.close(fig)
    return output.getvalue()


def graph_generator():
    """Graph output as video feed"""
    while True:
        # get sample data
        output = make_thermometer_frame(imu.read_temperature())
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + output + b'\r\n')
        time.sleep(0.1)


@app.route('/')
def display():
    return Response(graph_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
