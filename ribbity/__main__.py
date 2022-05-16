"""
Command-line interface.
"""
import click
from .main_pull import main as main_pull
from .main_build import main as main_build

@click.group
def cli():
    pass

@click.command()
@click.argument("configfile", default="site-config.toml")
def pull(configfile):
    "pull issues from repository to local"
    return main_pull(configfile)


@click.command()
@click.argument("configfile", default="site-config.toml")
def build(configfile):
    "build from local issues to mkdocs site"
    return main_build(configfile)


cli.add_command(pull)
cli.add_command(build)

    
def main():
    cli()


if __name__ == "__main__":
    main()
