import click

from textwrap import TextWrapper


def echo_dict(data, no_color, key_color='green', spaces=None, value_color='blue'):
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

        click.echo(
            ''.join([
                style_string(title, no_color, fg=key_color),
                wrapper.fill(style_string(value, no_color, fg=value_color))
            ])
        )


def echo_style(message, no_color, fg='yellow'):
    if no_color:
        click.echo(message)
    else:
        click.secho(message, fg=fg)


def get_max_key(data):
    return max(map(len, data))


def style_string(message, no_color, fg='yellow'):
    if no_color:
        return message
    else:
        return click.style(message, fg=fg)
