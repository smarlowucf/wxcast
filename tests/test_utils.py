from wxcast.utils import echo_dict, echo_style, get_max_key, style_string


def test_echo_dict(capsys):
    data = {'Test': 'Data', 'Is': 'Great'}
    echo_dict(data, False)

    out, err = capsys.readouterr()
    assert out == "Test:  Data\n  Is:  Great\n"


def test_echo_style(capsys):
    msg = 'Test data message!'
    echo_style(msg, False)

    out, err = capsys.readouterr()
    assert out == 'Test data message!\n'

    echo_style(msg, True)

    out, err = capsys.readouterr()
    assert out == 'Test data message!\n'


def test_max_key():
    data = {'Test': 'Data', 'Is': 'Great'}
    val = get_max_key(data)
    assert val == 4


def test_style_string():
    msg = 'Test data message!'

    styled_msg = style_string(msg, False)
    assert styled_msg == '\x1b[33mTest data message!\x1b[0m'

    styled_msg = style_string(msg, True)
    assert styled_msg == 'Test data message!'
