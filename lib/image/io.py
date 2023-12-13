from PIL import Image
import numpy as np

class ImagePixelData:
    def __init__(self, pixels: np.ndarray):
        if pixels.dtype != np.uint8:
            raise Exception(f"Only uint8 images are supported, {pixels.dtype} is not supported")
        if np.any(np.round(pixels.astype(float))!= pixels):
            raise Exception("Only uint8 images are supported. Found non-integer values")
        if np.any(pixels < 0) or np.any(pixels > 255):
            raise Exception("Only uint8 images are supported, found values outside of the range of 0-255")
        if pixels.ndim not in [2, 3]:
            raise Exception("Only L, RGB, and RGBA images are supported, found {pixels.ndim} dimensions")
        if pixels.ndim == 3 and pixels.shape[-1] not in [1, 3, 4]:
            raise Exception("Only L, RGB, and RGBA images are supported, found {pixels.ndim} dimensions with {pixels.shape[-1]} channels")
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

    def to_rgba(self) -> "ImagePixelData":
        self.initial_mode = "RGBA"
        if self.pixels.shape[-1] == 1:
            L = self.pixels[:,:,0]
            self.pixels = np.dstack((L, L, L, np.full_like(L, 255)))
        if self.pixels.shape[-1] == 3:
            R = self.pixels[:,:,0]
            G = self.pixels[:,:,1]
            B = self.pixels[:,:,2]
            self.pixels = np.dstack((R, G, B, np.full_like(R, 255)))
        return self    

    def to_rgb(self) -> "ImagePixelData":
        self.initial_mode = "RGB"
        if self.pixels.shape[-1] == 1:
            L = self.pixels[:,:,0]
            self.pixels = np.dstack((L, L, L))
        if self.pixels.shape[-1] == 4:
            R = self.pixels[:,:,0]
            G = self.pixels[:,:,1]
            B = self.pixels[:,:,2]
            self.pixels = np.dstack((R, G, B))
        return self    

    def to_l(self) -> "ImagePixelData":
        self.initial_mode = "L"
        if self.pixels.shape[-1] == 3:
            R = self.pixels[:,:,0].astype(float)
            G = self.pixels[:,:,1].astype(float)
            B = self.pixels[:,:,2].astype(float)
            mean_rgb = np.mean(np.dstack((R, G, B)), axis=-1).astype(np.uint8)
            self.pixels = np.dstack((mean_rgb,))
        if self.pixels.shape[-1] == 4:
            R = self.pixels[:,:,0].astype(float)
            G = self.pixels[:,:,1].astype(float)
            B = self.pixels[:,:,2].astype(float)
            A = self.pixels[:,:,3].astype(float)
            mean_rgb = np.mean(np.dstack((R, G, B)), axis=-1)
            scale_factor = np.divide(A, 255)
            scaled_pixels = np.multiply(mean_rgb, scale_factor)
            scaled_pixels_uint8 = scaled_pixels.astype(np.uint8)
            self.pixelsspace = np.dstack((scaled_pixels_uint8,))

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
        pil_image = Image.open(path)
        if pil_image.mode not in ["L", "RGB", "RGBA"]:
            raise Exception(f"Only L, RGB, and RGBA images are supported, {pil_image.mode} is not supported")
        return cls(np.asarray(pil_image))
