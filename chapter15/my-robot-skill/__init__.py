from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import requests


class MyRobot(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.base_url = self.settings.get("base_url")

    @intent_handler(IntentBuilder("")
                    .require("Robot")
                    .require("TestRainbow"))
    def handle_test_rainbow(self, message):
        try:
            requests.post(self.base_url + "/run/test_rainbow")
            self.speak_dialog('Robot')
            self.speak_dialog('TestingRainbow')
        except:
            self.speak_dialog("UnableToReach")
            LOG.exception("Unable to reach the robot")


def create_skill():
    return MyRobot()

