# Vapoursynth Portable Installation Tutorial for Windows (WIP)
A short Guide to install Vapoursynth Portable, as well as everything one needs to get started.

<br />

## 1. Install Vapoursynth Portable
1. Download the latest `Install-Portable-VapourSynth-RXX.ps1` from the [official Vapoursynth GitHub](https://github.com/vapoursynth/vapoursynth/releases).
2. Place the file in the directory where you want your Vapoursynth Portable folder to be.
3. Execute the file by right-clicking it and selecting "Run with PowerShell". This will first install Python, followed by Vapoursynth. Since everything is portable, it will not interfere with any other Python versions you may have installed on your system.
4. Follow the instructions in the console.
5. That's it! A new folder named `vapoursynth-portable` should appear. You can now delete the `.ps1` file.

<br />

## 2. Install a Source Plugin
Source plugins are required to read video files. Bestsource is the most commonly used option.
1. Download the latest `BestSource-RX.7z` from the [official BestSource GitHub](https://github.com/vapoursynth/bestsource/releases).
2. Unzip if needed and place the `.dll` file in your `vapoursynth-portable/vs-plugins` folder.

<br />

## 3. Install an Encoder
Encoders are required to write video files. FFmpeg is the most commonly used option.
1. Download the latest version of FFmpeg from the [official FFmpeg website](https://ffmpeg.org/download.html). In the "Get packages & executable files" section, click on Windows and choose a distributor. Ensure the file you download does __not__ have "shared" in its name.
2. Unzip if needed and place the `ffmpeg.exe` into your `vapoursynth-portable` folder.
3. That's it! You can delete any other files that came with FFmpeg.
 
> [!TIP]
> Example command to encode a Vapoursynth script. You must be in the same folder as your `vspipe.exe`:  
> `vspipe -c y4m "example_script.vpy" - | ffmpeg -i - -c:v libx264 -crf 16 -preset slow "output.mkv"`

> [!TIP]
> If you add `vspipe.exe` and `ffmpeg.exe` to your Windows PATH, you can use them from any directory.

<br />

## 4. Install Vapoursynth Editor and Previewer
1. Download the latest `VapourSynth.Editor-r19-mod-X.X.zip` and `VC_redist.x64.exe` from [GitHub](https://github.com/YomikoR/VapourSynth-Editor).
2. Install `VC_redist.x64.exe`, then unzip all files from the zip into the `vapoursynth-portable` folder.
3. That's it! You can now delete the zip file and run the editor using the `vsedit.exe`.

> [!TIP]
> Press F5 in the editor to open or refresh the preview window. A working Vapoursynth script is required to open the preview.

<br />

## 5. Your first Vapoursynth Project
Every Vapoursynth script needs a few things. Shown here in this simple example. Save it as either a `.vpy` or `.py` file and try previewing it with the Vapoursynth Editor.

```python

### 1. initialize vapoursynth
# imports vapoursynth into this script
import vapoursynth as vs

# get the core object, which acts like the engine for all vapoursynth operations
core = vs.core


### 2. load video clips
# load a video clip into the script and give it the name "clip"
# let's assume it is a common video in YUV format, 420 chroma subsampling and a bit depth of 8.
# if you don't know what this is, chatgpt can help to explain the basics.
clip = core.bs.VideoSource(source="path/to/your_video.mp4")


### 3. filter the clip
# you can now filter the clip in various ways.
# as an example we will first resize it to 1280x720, add a blur, then do a format conversion.
# for more information on each filter, check the official documentation: http://www.vapoursynth.com/doc/functions/video/resize.html

# it is good common pratice to convert the clip to 16bit first.
# doing filtering in higher bit depth reduces banding and other artifacts.
# this converts the input clip from YUV420P8 to YUV420P16.
# YUV is the format, 420 the chroma subsampling, P is progressive, and 16 is the bit depth.
clip = core.resize.Bilinear(clip, format=vs.YUV420P16)

# resize the clip to 1280x720
clip = core.resize.Bilinear(clip, width=1280, height=720)

# add a simple box blur to the clip
clip = core.std.Boxblur(clip, hradius=10, hpasses=3, vradius=10, vpasses=3)


### output the video clip ###
# specify that this final clip is what the script will output
clip.set_output()
```

<br />

## 6. Install Additional Vapoursynth Plugins
Installing Vapoursynth plugins is straightforward: download and place them in the correct folder.  
If you are looking for specific plugins, or just want to see what is available, the [Vapoursynth Database (VSDB)](https://vsdb.top/) makes it very easy. Not everything is listed there, but a lot!
1. Download the plugin. You can download directly from VSDB, but it's recommended to check the GitHub link for potentially more up-to-date versions. On GitHub, you can find download links on the right in the "Releases" section.
2. Unzip if needed and place the `.dll` file in your `vapoursynth-portable/vs-plugins` folder.
3. That's it! You can now use the plugin in Vapoursynth.
 
> [!TIP]
> Rarely a plugin has additional dependencies, or special installation instructions. These are usually detailed in the GitHub README or on the download page.

> [!TIP]
> If you are seeing an error message similar to this one, you are missing a plugin, or one of its dependencies:  
> `AttributeError: No attribute with the name mv exists. Did you mistype a plugin namespace?`  
> In this case we are missing mvtools indicated by the mv.

<br />






















## 7. Install Additional Vapoursynth Scripts
Installing Vapoursynth scripts is similar to plugin installation.  
If you are looking for specific scripts, or just want to see what is available, the [Vapoursynth Database (VSDB)](https://vsdb.top/) makes it very easy. Not everything is listed there, but a lot!
1. Download the script. You can download directly from VSDB, but it's recommended to check the GitHub link for potentially more up-to-date versions. On GitHub, you can find download links on the right in the "Releases" section. If no "Releases" section exists, click the green "Code" button and select "Download Zip".
3. If the script comes in a zip file, unzip it.
4. If it's a single `.py` file, place it directly in the `vapoursynth-portable/vs-scripts` folder.  
   If it's a folder containing multiple `.py` files or subfolders, place the entire folder in the `vapoursynth-portable/vs-scripts` folder.
5. Scripts often depend on plugins, python packages, or other scripts. Check the GitHub README or download page for details.
6. That's it! You can now use the script in Vapoursynth.

> [!TIP]
> Scripts often have additional dependencies. These are usually detailed in the GitHub README or on the download page.

> [!TIP]
> If you are seeing an error message similar to this one, you are missing a script, python package, or one of its dependencies:  
> `ModuleNotFoundError: No module named 'numpy'`  
> In this case we are missing the python package numpy.

<br />

## 8. Install Additional Python Packages for Vapoursynth
Some scripts require additional Python packages to work. As an example we will use the numpy package, which is often needed.
1. Open your vapoursynth-portable folder.
2. Click on the address bar at the top (where the folder path is shown), type `cmd`, and press Enter. This will open the console at the location of the vapoursynth-portable folder.
3. Since we are using a portable Python, we need to adjust the common pip commands you will find on the internet a little.  
Common: `pip install numpy`  
Adjusted: `python -m pip install numpy`  
By adding "python -m" in front, we point to the python version inside the vapoursynth-portable folder.
4. That's it! You can now use the python package in Vapoursynth.

> [!TIP]
> Here is an additional example with pytorch:  
> common: `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126`  
> adjusted: `python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126`
