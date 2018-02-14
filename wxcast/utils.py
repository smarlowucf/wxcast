import click

from textwrap import TextWrapper


def echo_dict(data,
              no_color,
              key_color='green',
              spaces=None,
              value_color='blue'):
    """
    Echoes a dictionary pretty-print style to terminal.

    :param data: The dictionary of key:vals to print.
    :param no_color: If true prints formatted but with no ascii color.
    :param key_color: Color for dictionary keys.
    :param spaces: Number of spaces to offset values. Max length of keys.
    :param value_color: Color for values.
    """
    if not spaces:
        spaces = get_max_key(data)

    for key, value in data.items():
        title = '{spaces}{key}:  '.format(
            spaces=' ' * (spaces - len(key)),
            key=key
        )
        wrapper = TextWrapper(
            width=(82 - spaces),
            subsequent_indent=' ' * (spaces + 3)
        )

        if isinstance(value, dict):
            echo_dict(value, no_color, key_color, spaces, value_color)
        else:
            click.echo(
                ''.join([
                    style_string(title, no_color, fg=key_color),
                    wrapper.fill(style_string(value, no_color, fg=value_color))
                ])
            )


def echo_style(message, no_color, fg='yellow'):
    """
    Echo string with style if no_color is False.

    :param message: String to echo.
    :param no_color: If True echo without style.
    :param fg: String style color.
    """
    if no_color:
        click.echo(message)
    else:
        click.secho(message, fg=fg)


def get_max_key(data):
    """
    Get the max key length from dictionary.

    :param data: Dictionary of key values.
    :return: Max length of dictionary key as int.
    """
    return max(map(len, data))


def style_string(message, no_color, fg='yellow'):
    """
    Add color style to string if no_color is False.

    :param message: String to style.
    :param no_color: If True return string without style.
    :param fg: The color for the string style.
    :return: Return string conditionally style.
    """
    if no_color:
        return message
    else:
        return click.style(message, fg=fg)
