
# Ubuntu with tensorrt as base image
# https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorrt/tags
FROM nvcr.io/nvidia/tensorrt:25.06-py3
ARG DEBIAN_FRONTEND=noninteractive

# Update apt
RUN apt-get -y update
RUN apt -y update

# Install dependencies
RUN apt-get install -y \
    p7zip-full x264 autoconf libtool yasm nasm clang ffmsindex libffms2-dev wget \
    pkg-config build-essential manpages-dev software-properties-common \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev curl libncursesw5-dev \
	xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
	checkinstall qt6-base-dev libqt6websockets6-dev libqt6core5compat6-dev\
	ocl-icd-opencl-dev libboost-dev libboost-system-dev libboost-filesystem-dev \
    x11-xserver-utils libxcb-cursor0 xfe libfftw3-dev libturbojpeg big-cursor

# Upgrade pip and install Python packages
RUN python -m pip install --upgrade pip && \
    python -m pip install Cython meson ninja setuptools wheel \
	onnx onnxruntime onnxruntime-gpu \
    opencv-python Pillow tensorboardX pyiqa einops positional_encodings timm PyTurboJPEG

# Install torch
RUN python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install mmcv from source with support for 10-50 series gpus
ENV MMCV_WITH_OPS=1 FORCE_CUDA=1 TORCH_CUDA_ARCH_LIST="6.1;7.5;8.6;8.9;12.0"
RUN python -m pip install --no-cache-dir --force-reinstall --no-binary mmcv "mmcv>=2.0.0" --ignore-installed PyYAML

# Install FFmpeg7
RUN add-apt-repository ppa:ubuntuhandbook1/ffmpeg7 && \
    apt-get update && apt-get install -y ffmpeg libavcodec-dev

# Install zimg
RUN git clone https://github.com/sekrit-twc/zimg --recursive && cd zimg && \
    ./autogen.sh && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd .. && rm -rf zimg

# Install VapourSynth
RUN wget https://github.com/vapoursynth/vapoursynth/archive/refs/tags/R72.tar.gz && \
    tar -zxvf R72.tar.gz && mv vapoursynth-R72 vapoursynth && cd vapoursynth && \
    ./autogen.sh && \
	./configure --prefix=/usr/local && \
    make -j$(nproc) && \
	make install && \
	ldconfig && \
    cd .. && rm -rf vapoursynth R72.tar.gz
RUN python -m pip install vapoursynth

# Install BestSource
RUN apt-get install libxxhash-dev -y && \
    git clone https://github.com/vapoursynth/bestsource --depth 1 --recurse-submodules --shallow-submodules && \
    cd bestsource && \
    CFLAGS=-fPIC meson setup -Denable_plugin=true build && \
    CFLAGS=-fPIC ninja -C build && ninja -C build install && \
    cd .. && rm -rf bestsource

# Install FFMS2
RUN git clone https://github.com/FFMS/ffms2 && cd ffms2 && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local \
                --libdir=/usr/local/lib/vapoursynth \
                --enable-vapoursynth && \
    make -j$(nproc) && make install && \
    cd .. && rm -rf ffms2

# Install lsmash
RUN git clone https://github.com/l-smash/l-smash && \
    cd l-smash && CFLAGS=-fPIC CXXFLAGS=-fPIC LDFLAGS="-Wl,-Bsymbolic" \
        ./configure --enable-shared --extra-ldflags="-Wl,-Bsymbolic" && \
    make -j$(nproc) && make install && \
    cd .. && rm -rf l-smash && \
    git clone https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works && \
    cd L-SMASH-Works/VapourSynth && \
    meson build && ninja -C build && ninja -C build install && \
    cd ../../.. && rm -rf L-SMASH-Works

# Upgrade CMake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.28.0-rc1/cmake-3.28.0-rc1-linux-x86_64.sh && \
    chmod +x cmake-3.28.0-rc1-linux-x86_64.sh && \
    sh cmake-3.28.0-rc1-linux-x86_64.sh --skip-license && \
    cp /workspace/bin/cmake /usr/bin/cmake && \
    cp /workspace/bin/cmake /usr/lib/x86_64-linux-gnu/cmake && \
    cp /workspace/bin/cmake /usr/local/bin/cmake && \
    cp -r /workspace/share/cmake-3.28 /usr/local/share/ && \
    rm cmake-3.28.0-rc1-linux-x86_64.sh && \
    rm -rf cmake-3.28.0-rc1-linux-x86_64

# Install vs-mlrt
RUN git clone --depth 1 https://github.com/AmusementClub/vs-mlrt && \
    cd vs-mlrt/vstrt && mkdir build && cd build && \
    CXXFLAGS="-I/usr/local/include/vapoursynth" \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DVAPOURSYNTH_INCLUDE_DIRECTORY=/usr/local/include \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DCMAKE_INSTALL_LIBDIR=lib/vapoursynth && \
    make -j$(nproc) && make install && \
    cd ../../../ && rm -rf vs-mlrt

# Setup Qt6
ENV PATH="/usr/lib/qt6/bin:$PATH" \
    XDG_RUNTIME_DIR=/tmp/runtime-root
	
# Install vsedit
RUN git clone https://github.com/YomikoR/VapourSynth-Editor && \
    cd VapourSynth-Editor/pro && \
    qmake pro.pro && \
    make && \
    mv ../build/release-64bit-gcc/vsedit /usr/local/bin/ && \
    mv ../build/release-64bit-gcc/vsedit-* /usr/local/bin/ && \
    cd ../.. && rm -rf VapourSynth-Editor

# Clean up unnecessary files
RUN apt-get autoclean -y && apt-get autoremove -y && apt-get clean -y && \
    python -m pip cache purge

# Create symbolic links for vsedit and xfe config files so that they don't reset
RUN mkdir -p /root/.config/xfe \
    && ln -sf /workspace/vapoursynth/configs/vsedit.config /root/.config/vsedit.config \
    && ln -sf /workspace/vapoursynth/configs/xfwrc /root/.config/xfe/xfwrc \
    && ln -sf /workspace/vapoursynth/configs/xferc /root/.config/xfe/xferc

# Remove Nvidia banner text wall
RUN rm -f /opt/nvidia/entrypoint.d/*banner* /opt/nvidia/entrypoint.d/*.txt

# Run startup script if available
CMD ["/bin/bash", "-c", "\
  STARTUP=/workspace/vapoursynth/configs/startup.sh && \
  if [ -f \"$STARTUP\" ]; then \
    chmod +x \"$STARTUP\" && \
    exec \"$STARTUP\"; \
  else \
    echo 'Warning: Startup config not found in configs/startup.sh' && \
    cd /workspace/vapoursynth && \
    exec /bin/bash; \
  fi"]