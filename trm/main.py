import click
import os
import configparser

from trm.sanitiser import sanitise
from trm.parser import MarkdownParser


CONFIG_FILENAME = '.trm'


def get_config(path):
    return os.path.join(path, CONFIG_FILENAME)


CONFIG_PATH = [get_config(path) for path in (
    os.path.realpath('./'),
    os.path.expanduser('~/'),
)]


@click.command()
@click.argument('note', type=click.File('r'))
@click.option('-c', '--config', default=None, type=click.File('rb'))
@click.option('-v', '--verbose', count=True)
def trm(note, config, verbose):
    path = get_config(os.path.dirname(note.name))

    paths = CONFIG_PATH + [path]
    if config is not None:
        paths.append(config)
    config = configparser.ConfigParser()
    config.read(paths)

    lines = sanitise(note.readlines())

    markdown = MarkdownParser(lines)
    elements_tree = markdown.parse()

    if verbose:
        click.echo(elements_tree)


if __name__ == '__main__':
    trm()
