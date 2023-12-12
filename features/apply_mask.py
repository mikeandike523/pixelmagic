import traceback

import click
from termcolor import colored
import numpy as np

from lib.image.io import ImagePixelData

@click.command()
@click.option('--input', default=None, type=str, help='Path to the input image')
@click.option('--output', default=None, type=str, help='Path to the output image')
@click.option('--mask', default=None, type=str, help='Path to the mask image')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose output')

def unsafe_apply_mask(input, output, mask):
    input_data = ImagePixelData.load(input)
    mask_data = ImagePixelData.load(mask)
    mask_R = mask_data.get_pixels()[:,:,0]
    mask_boolean = mask_R > 0
    input_pixels = input_data.get_pixels()
    if input_pixels.shape[-1] == 1:
        input_pixels_L = input_pixels[:,:,0]
        masked_input_pixels_L = np.where(mask_boolean, input_pixels_L, np.zeros_like(input_pixels_L))
        masked_pixels = np.dstack((masked_input_pixels_L,))
    elif input_pixels.shape[-1] == 3:
        input_pixels_R = input_pixels[:,:,0]
        input_pixels_G = input_pixels[:,:,1]
        input_pixels_B = input_pixels[:,:,2]
        masked_input_pixels_R = np.where(mask_boolean, input_pixels_R, np.zeros_like(input_pixels_R))
        masked_input_pixels_G = np.where(mask_boolean, input_pixels_G, np.zeros_like(input_pixels_G))
        masked_input_pixels_B = np.where(mask_boolean, input_pixels_B, np.zeros_like(input_pixels_B))
        masked_pixels = np.dstack((masked_input_pixels_R, masked_input_pixels_G, masked_input_pixels_B))
    elif input_pixels.shape[-1] == 4:
        input_pixels_R = input_pixels[:,:,0]
        input_pixels_G = input_pixels[:,:,1]
        input_pixels_B = input_pixels[:,:,2]
        input_pixels_A = input_pixels[:,:,3]
        masked_input_pixels_R = np.where(mask_boolean, input_pixels_R, np.zeros_like(input_pixels_R))
        masked_input_pixels_G = np.where(mask_boolean, input_pixels_G, np.zeros_like(input_pixels_G))
        masked_input_pixels_B = np.where(mask_boolean, input_pixels_B, np.zeros_like(input_pixels_B))
        masked_input_pixels_A = np.where(mask_boolean, input_pixels_A, np.zeros_like(input_pixels_A))
        masked_pixels = np.dstack((masked_input_pixels_R, masked_input_pixels_G, masked_input_pixels_B, masked_input_pixels_A))
    else:
        raise Exception("Only single channel, RGB, or RGBA images are supported")
    masked_data = ImagePixelData(masked_pixels)
    masked_data.save(output)


def apply_mask(input, output, mask, verbose=False):
    """
    @todo
    """
    try:
        unsafe_apply_mask(input, output, mask)
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

if __name__ == '__main__':
    apply_mask()