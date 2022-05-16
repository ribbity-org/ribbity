import click
from .main_pull import main as main_pull
from .main_build import main as main_build

@click.group
def cli():
    pass

@click.command()
@click.argument("configfile")
def pull(configfile):
    return main_pull(configfile)


@click.command()
@click.argument("configfile")
def build(configfile):
    return main_build(configfile)


cli.add_command(pull)
cli.add_command(build)

    
def main():
    cli()


if __name__ == "__main__":
    main()
