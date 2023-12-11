import traceback
import warnings

import click
from termcolor import colored
import cv2
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

INTERPOLATION_CHOICES=['area', 'cubic', 'linear']
def get_cv2_interpolation(interpolation):
    if interpolation.lower() not in INTERPOLATION_CHOICES:
        raise Exception("Interpolation must be one of the following: {}".format(INTERPOLATION_CHOICES))
    return interpolation.lower()

def is_whole(num):
    return round(num) == num

def unsafe_resize(i, o, factor_x, factor_y, factor_xy, interpolation):
    if factor_x is not None and factor_xy is not None:
        raise Exception("Both factor-x and factor-xy cannot be specified at the same time")
    if factor_y is not None and factor_xy is not None:
        raise Exception("Both factor-y and factor-xy cannot be specified at the same time")
    if factor_xy is None:
        if factor_x is None or factor_y is None:
            raise Exception("Both factor-x and factor-y must be specified when factor-xy is not specified")
    true_factor_x = factor_x if factor_x is not None else factor_xy
    true_factor_y = factor_y if factor_y is not None else factor_xy
    if not true_factor_x or not true_factor_y:
        raise Exception("Unable to determine the resizing factor in the x and y directions")
    pixels = np.asarray(Image.open(i))
    if np.any(np.round(pixels)!=pixels):
        raise Exception("Only uint8 encoded images are supported")
    if np.any(pixels < 0):
        raise Exception("Only uint8 encoded images are supported")
    if np.any(pixels > 255):
        raise Exception("Only uint8 encoded images are supported")
    if pixels.ndim not in [2, 3]:
        raise Exception("Only single channel, RGB, or RGBA images are supported")
    original_mode="RGBA"
    if pixels.ndim == 2:
        original_mode="L"
        pixels = np.expand_dims(pixels, axis=2)
    if pixels.shape[2] == 3:
        original_mode="RGB"
        R = pixels[:, :, 0]
        G = pixels[:, :, 1]
        B = pixels[:, :, 2]
        A = np.full_like(R, 255)
        pixels = np.dstack((R, G, B, A))
    W = pixels.shape[1]
    H = pixels.shape[0]
    resized_W = W * true_factor_x
    resized_H = H * true_factor_y
    if not is_whole(resized_W):
        warnings.warn(colored(f"Warning: the factor {true_factor_x} does not evenly divide the width {W}. The resize width is determined by rounding", "yellow"))
    if not is_whole(resized_H):
        warnings.warn(colored(f"Warning: the factor {true_factor_y} does not evenly divide the height {H}. The resize height is determined by rounding", "yellow"))
    resized_W = round(resized_W)
    resized_H = round(resized_H)
    # This allows the resize tool to be reused for converting file formats
    if true_factor_x == 1 and true_factor_y == 1:
        resized_pixels = pixels
    else:
        resized_pixels = cv2.resize(pixels, (resized_W, resized_H), interpolation=get_cv2_interpolation(interpolation))

    if original_mode == "RGBA":
        Image.fromarray(resized_pixels).save(o, mode=original_mode)
    elif original_mode == "RGB":
        R = resized_pixels[:, :, 0]
        G = resized_pixels[:, :, 1]
        B = resized_pixels[:, :, 2]
        RGB = np.dstack((R, G, B))
        Image.fromarray(RGB).save(o, mode=original_mode)
    elif original_mode == "L":
        L = resized_pixels[:, :, 0]
        Image.fromarray(L).save(o, mode=original_mode)
    else:
        raise Exception("Could not determine the format of the input image")

@click.command()
@click.option('--input', default=None, type=str, help='Path to the input file')
@click.option('--output', default=None, type=str, help='Path to the output file')
@click.option('--factor-x', default=None, type=int, help='Factor to resize the image by in the x direction')
@click.option('--factor-y', default=None, type=int, help='Factor to resize the image by in the y direction')
@click.option('--factor-xy', default=None, type=int, help='Factor to resize the image by (equally) in both directions')
@click.option("--interp", default="linear", type=click.Choice(INTERPOLATION_CHOICES), help="Interpolation method to use. Defaults to 'linear'.")
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose output')
def resize(input, output, factor_x, factor_y, factor_xy, interp, verbose=False):
    """
    @todo
    """
    try:
        unsafe_resize(input, output, factor_x, factor_y, factor_xy, interp)
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
    resize()
    