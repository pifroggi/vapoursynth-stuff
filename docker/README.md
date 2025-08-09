
# VapourSynth Docker Container
A VapourSynth docker image with many AI related features and set up to work similarly to a portable VapourSynth install.

<br />

## Features
* Ubuntu 24.04
* Python 3.12
* VapourSynth
* FFmpeg 7
* PyTorch
* TensorRT
* vs-mlrt
* mmcv
* VapourSynth Editor *(type vsedit to run)*
* X File Explorer *(type xfe to run)*
* Source Plugins: BestSource, FFMS2, L-SMASH-Works
* Various dependencies like: FFTW, Boost, OpenCV, libjpeg-turbo...
* Plugins in the vs-plugins folder are autoloaded.
* Scripts in the vs-scripts folder can be simply imported like: `import havfunc`
* GPU support
* optional GUI support
* Customization Options

<br />

## Requirements
* [Docker](https://www.docker.com/)
* [VcXsrv](https://sourceforge.net/projects/vcxsrv/) *(optional, only for GUI support)*
* Nvidia GPU with up-to-date drivers

<br />

## Setup
1. Run [VcXsrv](https://sourceforge.net/projects/vcxsrv/) with the default settings *(optional, only for GUI support)*
2. Download the `docker` folder from this GitHub repository
3. Open CMD or PowerShell in the `docker` folder or navigate into it
4. Run the docker container
   * __Option 1:__ Download a prebuild image  
     About 15gb download size and 25gb on disk.  
     When you run a docker container for the first time, it will be automatically downloaded.  
     If you don't need GUI support, remove `-e DISPLAY=host.docker.internal:0.0`
       ```
       # CMD:
       docker run -e DISPLAY=host.docker.internal:0.0 --privileged --gpus all -it -v "%cd%:/workspace/vapoursynth" pifroggi/vapoursynth:2025_07_28
       # PowerShell:
       docker run -e DISPLAY=host.docker.internal:0.0 --privileged --gpus all -it -v "${PWD}:/workspace/vapoursynth" pifroggi/vapoursynth:2025_07_28
       ```
   * __Option 2:__ Build the image yourself  
     About 30-60 minutes, depending on CPU and internet speed.  
     ```
     docker build -t vapoursynth .
     ```
     Once complete, run it like this. If you don't need GUI support, remove `-e DISPLAY=host.docker.internal:0.0`
       ```
       # CMD:
       docker run -e DISPLAY=host.docker.internal:0.0 --privileged --gpus all -it -v "%cd%:/workspace/vapoursynth" vapoursynth
       # PowerShell:
       docker run -e DISPLAY=host.docker.internal:0.0 --privileged --gpus all -it -v "${PWD}:/workspace/vapoursynth" vapoursynth
       ```

<br />

## Customization Options
All VapourSynth Editor and X File Explorer settings are saved to the configs folder and not lost when the container restarts.

### Default Paths
The vs-plugins folder path can be adjusted in configs/vapoursynth.conf  
The vs-scripts folder path can be adjusted in configs/startup.sh

### Startup Script
Every time the docker container is run, the script in configs/startup.sh is executed. You can edit it to your needs. For example if you would like the VapourSynth Editor to start automatically, simply add a line that says `vsedit`.

### DPI settings and Cursor size
DPI settings and cursor size can be adjusted for high resolution monitors.
1. Change Windows scaling behavior for VcXsrv.
    * Find `vcxsrv.exe` likely in `C:\Program Files\VcXsrv`
    * Right-click > Properties > Compatibility > Change high DPI settings
    * Check Override high DPI scaling behavior and set to: Application
2. Adjust settings. Defaults are for 1080p. For 4K I simply doubled all numbers.
    * In configs/startup.sh adjust:  
      `Xft.dpi: 96`  
      `Xcursor.size: 24`  
    * In configs/xferc adjust:  
      `screenres=100`

<br />
