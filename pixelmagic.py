import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import click

from features.resize import resize
from features.apply_mask import apply_mask

@click.group()
def cli():
    """
    @todo
    """

cli.add_command(resize)
cli.add_command(apply_mask)

if __name__ == '__main__':
    cli()


    
        

