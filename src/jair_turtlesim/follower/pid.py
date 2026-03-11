def limit(_value: float, _min: float, _max: float) -> float:
    _value = max(_min, _value)
    _value = min(_max, _value)
    return _value


# pylint: disable=too-few-public-methods
class PID:
    def __init__(self, p: float = 0.8, i: float = 0.01, d: float = 0.05):
        self._output_limit = 4.0
        self._p = p
        self._d = d
        self._i = i
        self._i_growing = 0.0
        self._last_error = 0.0

    def calc(self, error: float) -> float:
        p_term = error * self._p
        self._i_growing += error * self._i
        d_term = (error - self._last_error) * self._d

        p_term = limit(p_term, -self._output_limit, self._output_limit)
        self._i_growing = limit(self._i_growing, -self._output_limit, self._output_limit)
        d_term = limit(d_term, -self._output_limit, self._output_limit)

        output = p_term + self._i_growing + d_term
        output = limit(output, -self._output_limit, self._output_limit)

        self._last_error = error
        return output
