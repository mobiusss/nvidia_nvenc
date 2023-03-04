# Install dependencies (replace XXX in libnvidia-encode-XXX, libnvidia-decode-XXX with your driver version)
# libnvidia-encode is part of the driver meta package so if your driver works fine you might already have it ! 
apt install -y \
          libavfilter-dev \
          libavformat-dev \
          libavcodec-dev \
          libswresample-dev \
          libavutil-dev\
          wget \
          cmake \
          build-essential \
          git \
          libnvidia-encode-525 \
          libnvidia-decode-525 
# Install CUDA Toolkit (if not already present)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda
# Ensure nvcc to your $PATH (most commonly already done by the CUDA installation)
export PATH=/usr/local/cuda/bin:$PATH

# Install VPF
pip3 install git+https://github.com/NVIDIA/VideoProcessingFramework
# or if you cloned this repository
pip3 install .
