import torch
import torchvision.transforms as T
import PyNvCodec as nvc
import PytorchNvCodec as pnvc
import numpy as np

class cconverter:
    """
    Colorspace conversion chain.
    """

    def __init__(self, width: int, height: int, gpu_id: int):
        self.gpu_id = gpu_id
        self.w = width
        self.h = height
        self.chain = []

    def add(self, src_fmt: nvc.PixelFormat, dst_fmt: nvc.PixelFormat) -> None:
        self.chain.append(
            nvc.PySurfaceConverter(self.w, self.h, src_fmt, dst_fmt, self.gpu_id)
        )

    def run(self, src_surface: nvc.Surface) -> nvc.Surface:
        surf = src_surface
        cc = nvc.ColorspaceConversionContext(nvc.ColorSpace.BT_601, nvc.ColorRange.MPEG)

        for cvt in self.chain:
            surf = cvt.Execute(surf, cc)
            if surf.Empty():
                raise RuntimeError("Failed to perform color conversion")

        return surf.Clone(self.gpu_id)

def surface_to_tensor(surface: nvc.Surface) -> torch.Tensor:
    """
    Converts planar rgb surface to cuda float tensor.
    """
    if surface.Format() != nvc.PixelFormat.RGB_PLANAR:
        raise RuntimeError("Surface shall be of RGB_PLANAR pixel format")

    surf_plane = surface.PlanePtr()
    img_tensor = pnvc.DptrToTensor(
        surf_plane.GpuMem(),
        surf_plane.Width(),
        surf_plane.Height(),
        surf_plane.Pitch(),
        surf_plane.ElemSize(),
    )
    if img_tensor is None:
        raise RuntimeError("Can not export to tensor.")

    img_tensor.resize_(3, int(surf_plane.Height() / 3), surf_plane.Width())
    img_tensor = img_tensor.type(dtype=torch.cuda.FloatTensor)
    img_tensor = torch.divide(img_tensor, 255.0)
    img_tensor = torch.clamp(img_tensor, 0.0, 1.0)

    return img_tensor

def tensor_to_surface(img_tensor: torch.tensor, gpu_id: int) -> nvc.Surface:
    """
    Converts cuda float tensor to planar rgb surface.
    """
    if len(img_tensor.shape) != 3 and img_tensor.shape[0] != 3:
        raise RuntimeError("Shape of the tensor must be (3, height, width)")

    tensor_w, tensor_h = img_tensor.shape[2], img_tensor.shape[1]
    img = torch.clamp(img_tensor, 0.0, 1.0)
    img = torch.multiply(img, 255.0)
    img = img.type(dtype=torch.cuda.ByteTensor)

    surface = nvc.Surface.Make(nvc.PixelFormat.RGB_PLANAR, tensor_w, tensor_h, gpu_id)
    surf_plane = surface.PlanePtr()
    pnvc.TensorToDptr(
        img,
        surf_plane.GpuMem(),
        surf_plane.Width(),
        surf_plane.Height(),
        surf_plane.Pitch(),
        surf_plane.ElemSize(),
    )

    return surface

def rgb_converter( w, h, gpu_id=0):
    to_rgb = cconverter(w, h, gpu_id)
    to_rgb.add(nvc.PixelFormat.NV12, nvc.PixelFormat.YUV420)
    to_rgb.add(nvc.PixelFormat.YUV420, nvc.PixelFormat.RGB)
    to_rgb.add(nvc.PixelFormat.RGB, nvc.PixelFormat.RGB_PLANAR)
    return to_rgb

