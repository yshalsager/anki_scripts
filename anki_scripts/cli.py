import click


@click.group()
def cli():
    pass


@cli.command()
def tg_extract():
    """Command on cli"""
    pass
