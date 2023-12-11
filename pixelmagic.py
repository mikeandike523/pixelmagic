import click

from features.resize import resize

@click.group()
def cli():
    """
    @todo
    """

cli.add_command(resize)

if __name__ == '__main__':
    cli()


    
        

