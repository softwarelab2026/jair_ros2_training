from follower.tracker import normalize_ball_to_turtle_pos

def test_normalize_ball_to_turtle_pos_0_0():
    ball_pos = 0, 0

    norm_ball_x, norm_ball_y = normalize_ball_to_turtle_pos(ball_pos[0], ball_pos[1], 800, 800)

    assert norm_ball_x == 0.0
    assert norm_ball_y == 11.0

def test_normalize_ball_to_turtle_pos_0_800():
    ball_pos = 0, 800

    norm_ball_x, norm_ball_y = normalize_ball_to_turtle_pos(ball_pos[0], ball_pos[1], 800, 800)

    assert norm_ball_x == 0.0
    assert norm_ball_y == 0.0

def test_normalize_ball_to_turtle_pos_0_800():
    ball_pos = 800, 0

    norm_ball_x, norm_ball_y = normalize_ball_to_turtle_pos(ball_pos[0], ball_pos[1], 800, 800)

    assert norm_ball_x == 11.0
    assert norm_ball_y == 11.0

def test_normalize_ball_to_turtle_pos_800_800():
    ball_pos = 800, 800

    norm_ball_x, norm_ball_y = normalize_ball_to_turtle_pos(ball_pos[0], ball_pos[1], 800, 800)

    assert norm_ball_x == 11.0
    assert norm_ball_y == 0.0

