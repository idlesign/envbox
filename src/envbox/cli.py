import click

from envbox import VERSION, get_environment
from envbox.utils import MASKED_VALUE, is_secret_key


@click.group()
@click.version_option(version='.'.join(map(str, VERSION)))
def entry_point():
    """envbox command line utilities."""


@entry_point.command()
def probe():
    """Detect and print out current environment type."""
    env = get_environment()

    click.secho(f'Detected environment type: {env} ({env.__class__.__name__})')


@entry_point.command()
@click.option("--secrets", is_flag=True, help="Show sensitive values without masking.")
def show(*, secrets: bool):
    """Show (print out) current environment variables.

    Sensitive values (passwords, tokens, etc.) are masked
    unless --secrets flag is used.

    """
    env = get_environment()

    for key, val in sorted(env.env.items(), key=lambda item: item[0]):

        if not secrets and is_secret_key(key):
            val = MASKED_VALUE

        click.secho(f'{key} = {val}')


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()

