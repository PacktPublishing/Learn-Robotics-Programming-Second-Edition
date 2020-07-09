import time

from image_app_core import start_server_process, get_control_instruction, put_output_image
import pi_camera_stream

def controlled_image_server_behavior():
    camera = pi_camera_stream.setup_camera()
    time.sleep(0.1)

    for frame in pi_camera_stream.start_stream(camera):
        encoded_bytes = pi_camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)

        instruction = get_control_instruction()
        if instruction and instruction['command'] == "exit":
                print("Stopping")
                return

process = start_server_process('control_image_behavior.html')

try:
    controlled_image_server_behavior()
finally:
    process.terminate()
