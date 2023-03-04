# Install dependencies
# replace NV_DRIVER_VER with your driver version
NV_DRIVER_VER=525
KEY_PKG=cuda-keyring_1.0-1_all.deb

# Install CUDA Toolkit
KEY_URL=https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/$KEY_PKG
curl -X GET $KEY_URL > $KEY_PKG
sudo dpkg -i $KEY_PKG
sudo apt-get update

sudo apt install -y --no-install-recommends \
     python3-dev libavfilter-dev libavformat-dev \
     libavcodec-dev libswresample-dev libavutil-dev \
     wget cmake build-essential git cuda \
     libnvidia-encode-$NV_DRIVER_VER \
     libnvidia-decode-$NV_DRIVER_VER

# make a safe venv
python3 -m venv venv

# Ensure nvcc on $PATH (commonly already done by CUDA install)
export PATH=/usr/local/cuda/bin:$PATH

# Install VideoProcessingFramework
git clone https://github.com/NVIDIA/VideoProcessingFramework
venv/bin/pip install torch torchvision tqdm
venv/bin/pip install VideoProcessingFramework/. VideoProcessingFramework/src/PytorchNvCodec/.
	     
