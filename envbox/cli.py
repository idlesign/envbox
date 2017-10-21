#!/usr/bin/env python
import click

from envbox import VERSION, get_environment


@click.group()
@click.version_option(version='.'.join(map(str, VERSION)))
def entry_point():
    """envbox command line utilities."""


@entry_point.command()
def probe():
    """Detect and print out current environment type."""
    env = get_environment()

    click.secho('Detected environment type: %s (%s)' % (env, env.__class__.__name__))


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()

