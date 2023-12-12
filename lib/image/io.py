from PIL import Image
import numpy as np

class ImagePixelData:
    def __init__(self, pixels: np.ndarray):
        if pixels.dtype != np.uint8:
            raise Exception("Only uint8 images are supported")
        if np.any(np.round(pixels)!= pixels):
            raise Exception("Only uint8 images are supported")
        if np.any(pixels < 0) or np.any(pixels >= 255):
            raise Exception("Only uint8 images are supported")
        if pixels.ndim not in [2, 3]:
            raise Exception("Only L, RGB, and RGBA images are supported")
        if pixels.ndim == 3 and pixels.shape[-1] not in [1, 3, 4]:
            raise Exception("Only L, RGB, and RGBA images are supported")
        if pixels.ndim == 2:
            pixels = np.expand_dims(pixels, axis=-1)
            self.initial_mode="L"
        elif pixels.ndim == 3 and pixels.shape[-1] == 1:
            self.initial_mode="L"
        elif pixels.ndim == 3 and pixels.shape[-1] == 3:
            self.initial_mode="RGB"
        else:
            self.initial_mode="RGBA"
        self.pixels = pixels


    def get_pixels(self) -> np.ndarray:
        return self.pixels
    
    def get_initial_mode(self) -> str:
        return self.initial_mode
    
    def set_pixels(self, pixels: np.ndarray) -> "ImagePixelData":
        ipd = ImagePixelData(pixels)
        if ipd.get_initial_mode()!= self.get_initial_mode():
            raise Exception(f"Cannot change pixel data from {self.get_initial_mode()} to {ipd.get_initial_mode()}.")
        self.pixels = ipd.get_pixels()
        return self
    
    def save(self, path: str) -> None:
        Image.fromarray(self.pixels).save(path)

    @classmethod
    def load(cls, path: str) -> "ImagePixelData":
        return cls(np.array(Image.open(path)))