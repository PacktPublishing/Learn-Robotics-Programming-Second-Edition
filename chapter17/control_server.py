from flask import Flask, render_template, jsonify
from robot_modes import RobotModes

# A Flask App contains all its routes.
app = Flask(__name__)
# Prepare our robot modes for use
mode_manager = RobotModes()


@app.route("/")
def index():
    return render_template('menu.html', menu=mode_manager.menu_config)


@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # Use our robot app to run something with this mode_name
    mode_manager.run(mode_name)
    response = {'message': f'{mode_name} running'}
    if mode_manager.should_redirect(mode_name):
        response['redirect'] = True
    return jsonify(response)


@app.route("/stop", methods=['POST'])
def stop():
    # Tell our system to stop the mode it's in.
    mode_manager.stop()
    return jsonify({'message': "Stopped"})


app.run(host="0.0.0.0")
