# steps to install, roughly
* git clone https://github.com/NVIDIA/VideoProcessingFramework.git

* sh install.sh

* sudo apt-get install libavfilter-dev libavformat-dev libavcodec-dev libswresample-dev libavutil-dev

* pip install torch torchvision scikit-build

* cd VideoProcessingFramework/src/PytorchNvCodec

* PATH=/usr/local/cuda/bin:$PATH pip install . 

# contents of install.sh

See install.sh in the repo.

# acknowledgments

The VideoProcessingFramework repo is awesome!

As such, I didn't write the code I put into utils.py (it's from the VideoProcessingFramework repo).