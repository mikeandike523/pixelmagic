import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import click

from features.resize import resize
from features.apply_mask import apply_mask
from features.binarize_by_lightness import binarize_by_lightness

@click.group()
def cli():
    """
    @todo
    """

cli.add_command(resize)
cli.add_command(apply_mask)
cli.add_command(binarize_by_lightness)

if __name__ == '__main__':
    cli()


    
        

