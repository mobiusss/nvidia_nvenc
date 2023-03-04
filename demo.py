import argparse
import torch
import torchvision.transforms as T
import PyNvCodec as nvc
import tqdm

from utils import cconverter, surface_to_tensor, rgb_converter

def main( encFilePath: str,
          gpu_id:int = 0,
          resize:int = 128,
          max_frames:int = 1000 ) -> torch.Tensor:
    
    # init nvenc decoder
    nvDec = nvc.PyNvDecoder(encFilePath, gpu_id)
    w, h, N = nvDec.Width(), nvDec.Height(), nvDec.Numframes()
    N = min( max_frames, N )

    # init converters
    to_rgb = rgb_converter(w, h, gpu_id=gpu_id)
    tv_resizer = T.Resize((resize,resize))

    # decode and collect the tensors
    tensors = []
    progress = tqdm.tqdm(desc="decoding", total=N)
    while True and progress.n < max_frames:
        # Decode NV12 surface, cvt to planar RBG
        src_surface = nvDec.DecodeSingleSurface()
        if src_surface.Empty():
            break        
        rgb_pln = to_rgb.run(src_surface)
        if rgb_pln.Empty():
            break
        src_tensor = surface_to_tensor(rgb_pln)
        tensors.append( tv_resizer( src_tensor ) )
        progress.update(1)
    return torch.stack( tensors )

if __name__ == "__main__":
    print("This pytorch tensor load an input video on given GPU.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--inp","-i",default="vid.mp4")
    parser.add_argument("--gpu_id","-g",default=0, type=int)
    parser.add_argument("--resize","-r",default=128,type=int)
    parser.add_argument("--max_frames","-m", default=3000,type=int)
    args = parser.parse_args()
    res = main(args.inp,
               resize=args.resize,
               gpu_id=args.gpu_id,
               max_frames=args.max_frames)
    print("done")
