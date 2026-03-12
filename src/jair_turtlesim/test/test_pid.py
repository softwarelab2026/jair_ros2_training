from jair_turtlesim.follower.pid import PID


def test_pid_p():
    pid = PID(0.8, 0.0, 0.0, 99999999)
    
    result = pid.calc(10, 0.1)
    
    assert result == 8

def test_pid_d():
    pid = PID(0.0, 0.1, 0.0, 99999999)
    
    pid.calc(1, 0.1)
    result = pid.calc(10, 0.1)
    
    assert result == 0.9

def test_pid_i():
    pid = PID(0.0, 0.0, 0.01, 99999999)
    
    for _ in range(10):
        pid.calc(10, 0.1)
    result = pid.calc(10, 0.1)
    
    assert result == 0.11

def test_pid_i_wind_up_clamping():
    pid = PID(0.0, 0.0, 0.01, 400)
    
    for _ in range(9999):
        pid.calc(1, 0.1)
    
    result = pid.calc(-1, 0.1)
    
    assert result == 3.9989999999999997

def test_output_clamp():
    pid = PID(0.8, 0.05, 0.01, 4)
    
    for _ in range(10):
        pid.calc(10, 0.1)
    result = pid.calc(10, 0.1)
    
    assert result == 4.0

