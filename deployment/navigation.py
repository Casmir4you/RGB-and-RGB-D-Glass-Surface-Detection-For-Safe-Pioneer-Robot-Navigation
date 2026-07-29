import time


class GlassNavigationController:
    """
    Converts model navigation decisions into Pioneer robot movement.

    Expected commands:
    - MOVE_FORWARD
    - STOP
    - TURN_LEFT
    - TURN_RIGHT
    """

    def __init__(
        self,
        robot,
        forward_speed: float = 180.0,
        turn_angle_deg: float = 30.0,
        stop_delay_s: float = 0.5,
    ):
        self.robot = robot
        self.forward_speed = forward_speed
        self.turn_angle_deg = turn_angle_deg
        self.stop_delay_s = stop_delay_s

        self.last_command = None
        self.stopped_for_glass = False

    def execute(self, command: str) -> str:
        command = command.upper().strip()

        # Once glass is detected, stop and stay stopped
        if self.stopped_for_glass:
            self.robot.stop()
            return "Robot remains stopped after glass detection"

        if command == "STOP":
            self.robot.stop()
            self.stopped_for_glass = True
            self.last_command = command
            return "Robot stopped due to glass detection"

        if command == "MOVE_FORWARD":
            # Keep sending forward command every loop for physical robot reliability
            self.robot.move_forward(self.forward_speed)
            self.last_command = command
            return "Robot moving forward"

        # Ignore turning commands for controlled straight-line glass test
        if command in ["TURN_LEFT", "TURN_RIGHT"]:
            self.robot.move_forward(self.forward_speed)
            self.last_command = "MOVE_FORWARD"
            return f"Ignored {command}; robot continues forward"

        self.robot.stop()
        self.stopped_for_glass = True
        return f"Unknown command '{command}', robot stopped"