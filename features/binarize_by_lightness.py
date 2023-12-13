import traceback

import click
from termcolor import colored
import numpy as np

from lib.image.io import ImagePixelData

def unsafe_binarize_by_lightness(input, output, threshold):
    input_image = ImagePixelData.load(input)
    L_pixels = input_image.to_l().get_pixels()
    binarized_as_bool = L_pixels >= threshold
    binarized_as_uint8 = np.where(binarized_as_bool, 255, 0).astype(np.uint8)
    output_image = ImagePixelData(binarized_as_uint8)
    output_image.save(output)

@click.command()
@click.option('--input', default=None, type=str, help='Path to the input image')
@click.option('--output', default=None, type=str, help='Path to the output image')
@click.option('--threshold', default=None, type=float, help='Threshold (uint8) (0-255 inclusive) for the binarization')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose output')
def binarize_by_lightness(input, output, threshold, verbose=False):
    """
    Binarize an image by its lightness
    """
    try:
        unsafe_binarize_by_lightness(input, output, threshold)
    except Exception as e:
        if not verbose:
            print(colored("The program failed with the following error:", "red"))
            print(colored(str(e), "red"))
            exit(1)
        else:
            tb = traceback.format_exc()
            print(colored("The program failed with the following error:", "red"))
            print(colored(tb, "red"))
            exit(1) 
if __name__ == "__main__":
    binarize_by_lightness()