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

> [!TIP]
> To ensure exact frame perfect reading, an index will be automatically build for new video files. This may take a minute for very large files, but has to be done only once. No worries if nothing seems to happen at first or your previewer seems to freeze.

<br />

## 3. Install an Encoder
Encoders are required to write video files. FFmpeg is the most commonly used option.
1. Download the latest version of FFmpeg from the [official FFmpeg website](https://ffmpeg.org/download.html). In the "Get packages & executable files" section, click on Windows and choose a distributor. Ensure the file you download does __not__ have "shared" in its name.
2. Unzip if needed and place the `ffmpeg.exe` into your `vapoursynth-portable` folder.
3. That's it! You can delete any other files that came with FFmpeg.
 
> [!TIP]
> Example command to encode a Vapoursynth script. You must be in the same folder as your `vspipe.exe`:  
> `vspipe -c y4m "example_script.vpy" - | ffmpeg -i - -c:v libx264 -crf 16 -preset slow "output.mkv"`  
> __Warning:__ This command is for cmd and will not work in powershell.

> [!TIP]
> If you add `vspipe.exe` and `ffmpeg.exe` to your Windows PATH, you can use them from any directory.

<br />

## 4. Install Vapoursynth Editor and Previewer
1. Download the latest `VapourSynth.Editor-r19-mod-X.X.zip` and `VC_redist.x64.exe` from [GitHub](https://github.com/YomikoR/VapourSynth-Editor).
2. Install `VC_redist.x64.exe`, then unzip all files from the zip into the `vapoursynth-portable` folder.
3. That's it! You can now delete the zip file and run the editor using the `vsedit.exe`.

> [!TIP]
> Some nice functionality:
> * Press `F5` in the editor to open or refresh the preview window. (A working Vapoursynth script is required to open the preview.)
> * You can `right click` on the preview > `Save image` or `Copy to clipboard`
> * You can `scroll` trough the frames if your mouse is on the frame counter or timeline
> * `Middle mouse click` on preview changes the viewing mode between `native to your screen`, `zoom`, and `fill preview window`. Zoom factor and scaling algorithm is adjustable in the bottom right.
> * Output clip properties are shown at the very bottom of the preview window. For more info on each individual frame, `right click` on the preview > `Toggle frame properties panel`
> * If you set additional output clips like this, you can quickly compare them by `scrolling` on the bottom left `Index` dropdown:
> ```python
> clip.set_output(0)
> clip_denoised.set_output(1)
> clip_upscaled.set_output(2)
> ```




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
# as an example we will do a few format conversions, resize to 1280x720, and add a blur.
# for more information on each filter, check the official documentation: http://www.vapoursynth.com/doc/functions/video/resize.html

# it is good common pratice to convert the clip to 16bit first. doing filtering in bit depths higher than 8 reduces banding and other artifacts.
# this converts the input clip from YUV420P8 to YUV420P16. YUV is the format, 420 the chroma subsampling, and 16 is the bit depth.
# a list of all available formats can be found here: https://www.vapoursynth.com/doc/pythonreference.html#format
clip = core.resize.Bilinear(clip, format=vs.YUV420P16)

# resize the clip to 1280x720
clip = core.resize.Bilinear(clip, width=1280, height=720)

# add a simple box blur to the clip
clip = core.std.BoxBlur(clip, hradius=10, hpasses=3, vradius=10, vpasses=3)

# some filters require the input clip to be in RGB format. to convert a clip from YUV to RGB, a matrix coefficient is required.
# old SD sources from DVD/VHS often use 470bg (also known as 601), while modern sources use 709.
# see the bottom of the resize documentation for a full list: http://www.vapoursynth.com/doc/functions/video/resize.html
clip = core.resize.Bilinear(clip, format=vs.RGBS, matrix_in_s="709")

# convert from RGB back to YUV
clip = core.resize.Bilinear(clip, format=vs.YUV420P16, matrix_s="709")

### 4. output the video clip
# first convert it to the output format we want
clip = core.resize.Bilinear(clip, format=vs.YUV420P8)

# and lastly specify that the clip called "clip" is what the script should output
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

> [!TIP]
> Some people make their scripts installable as packages too. If you see this and would like to do that, adjust those commands too:  
> common: `pip install -U git+https://github.com/pifroggi/vs_colorfix.git`  
> adjusted: `python -m pip install -U git+https://github.com/pifroggi/vs_colorfix.git`  
> Scripts installed this way will be located in `\Lib\site-packages` instead of your scripts folder. 

<br />




























## 9. Common Errors
Some common issues when trying to use Vapoursynth.

---

__`Failed to initialize VSScript` when trying to encode a video using vspipe and ffmpeg.__  
* __Explanation:__ The error can have many causes, but in this specific situation it may be that you are accidentaly using a command made for CMD in Powershell. Powershell does not support everything CMD does and sometimes needs different commands.  
* __Solution:__ Try using CMD instead.

---

__`SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position XX-XX: truncated \uXXXX escape` when trying to read a video file.__  
* __Explanation:__ The file path is written using backslashes `\` and Python interprets them as escape characters.
* __Solution:__ Prefix the path with r `r"C:\path\to\video.mp4"` or replace backslashes with normal slashes `"C:/path/to/video.mp4"`.

---

__`AttributeError: module 'vapoursynth' has no attribute 'get_core'` when trying to import or use a function from a Vapoursynth script.__  

* __Explanation:__ You are using an old Vapoursynth script, which still uses `vs.get_core()` to initialize the Vapoursynth core. This was changed to `vs.core` in newer versions.
* __Solution:__ Open the script in question and replace `vs.get_core()` with `vs.core`. The line should be somewhere near the top and likely says `core = vs.get_core()` in full.

---

__`Analyse: Function does not take argument(s) named _global` or `Analyse: Function does not take argument(s) named _lambda` when trying to use a function from a Vapoursynth script.__  
* __Explanation:__ Some words like "global" are reserved in the Python language and can not be used as function arguments. In the past to circumvent this issue, an underscore was put in front of such arguments. But at some point this was changed to a trailing underscore like this: `global_`. Common accurances are when trying to use older versions of the `G41Fun` or `havsfunc` scripts.  
* __Solution:__ Open the script in question and replace all instances of `_global` with `global_`. Do the same if it happens with other arguments like `_lambda`.






















