# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (c) 2021 Sean Marlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
                    wrapper.fill(
                        style_string(
                            str(value), no_color, fg=value_color
                        )
                    )
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
