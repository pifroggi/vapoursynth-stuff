# Paired Dataset Helper
A script to sync and align LQ videos with their HQ counterparts to create paired video or image datasets.  
Optionally match colors, filter unwanted frames, add degredations, crop and resize.  
This is a full vapoursynth script ready to run, use as a template, or starting point.

## Requirements
* `pip install numpy`
* `pip install opencv-python`
* [vs_colorfix](https://github.com/pifroggi/vs_colorfix)
* [vs_align](https://github.com/pifroggi/vs_align)
* [vs_liif](https://github.com/pifroggi/vs_liif)
* [vs_iqa](https://github.com/pifroggi/vs_iqa)
* [tbilateral](https://github.com/dubhater/vapoursynth-tbilateral) (optional, only to create banding degredation)

## Setup
1. make sure all plugins are loaded and scripts are imported 
2. change source plugin if needed, this currently uses [bestsource](https://github.com/vapoursynth/bestsource)
3. look through the settings and paths and adjust them as needed

## Usage
Run the script like you would run a normal vapoursynth script. While running, folders for the LR and HR images will automatically be created at the set paths and images will be saved there.
The output video has the IQA scores and diff_threshold values overlayed on top and can be used to finetune them. Alternatively the overlayed values can be previewed with [vsedit](https://github.com/YomikoR/VapourSynth-Editor) or [vs-preview](https://github.com/Jaded-Encoding-Thaumaturgy/vs-preview).  
Example with vspipe and ffmpeg:

    vspipe -c y4m paired-dataset-helper.vpy - | ffmpeg -i - -c:v libx264 -crf 20 -preset veryfast "preview.mkv"

If you don't want to save the output preview video and would just like to save the LR and HR images, you can run it like this:

    vspipe -c y4m paired-dataset-helper.vpy - | ffmpeg -f yuv4mpegpipe -i - -f null -

If the image output paths already have files within them, nothing will be saved. This is to avoid overwriting or mixing datasets.

## Tips
IQA settings can be used to filter for good or bad frames. For example when setting it like this, only low quality LR frames that have a high quality HR match will be saved:

    HR_iqa              = True
    HR_iqa_metric       = 'hyperiqa'
    HR_iqa_threshold    = 0.5
    HR_iqa_mode         = 'lower'
    LR_iqa              = True
    LR_iqa_metric       = 'hyperiqa'
    LR_iqa_threshold    = 0.5
    LR_iqa_mode         = 'higher'
