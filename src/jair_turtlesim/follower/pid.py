import numpy as np


# pylint: disable=too-few-public-methods
class PID:
    def __init__(self, kp: float = 0.8, kd: float = 0.05, ki: float = 0.01):
        self._output_limit = 4.0
        self._kp = kp
        self._kd = kd
        self._ki = ki
        self._integral_sum = 0.0
        self._last_error = 0.0

    def calc(self, error: float, dt: float) -> float:
        p_term = error * self._kp
        self._integral_sum += error * dt
        d_term = (error - self._last_error) * self._kd

        self._integral_sum = np.clip(self._integral_sum, -self._output_limit, self._output_limit)

        i_term = self._integral_sum * self._ki
        output = p_term + i_term + d_term
        output = np.clip(output, -self._output_limit, self._output_limit)

        self._last_error = error
        return output
