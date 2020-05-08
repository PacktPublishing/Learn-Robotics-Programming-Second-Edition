import MPU9250

DMP_CTRL_1 = 0x6D
DMP_CTRL_2 = 0x6E
DMP_CTRL_3 = 0x6F

# DMP Register map
#   Tap and Android
ORIENT_EN       = 0x6AA
TAP_EN          = 0x81E
ORIENT_TAP_EN   = 0xAB9
TAP_AXES_EN     = 0x148

#   Pedometer


class MPU_DMP:
    def __init__(mpu_device):
        self.mpu_device = mpu_device

    def 