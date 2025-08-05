#!/bin/bash

# Set vapoursynth.conf location (has vs-plugins folder location in it)
export VAPOURSYNTH_CONF_PATH=/workspace/vapoursynth/configs/vapoursynth.conf

# Set vs-scripts folder location
export PYTHONPATH="/workspace/vapoursynth/vs-scripts:${PYTHONPATH}"


# Change DPI scaling and cursor size for high resolution monitors
echo "Xcursor.size: 24" | xrdb -merge # default 24
echo "Xft.dpi: 96"      | xrdb -merge # default 96


# Move to working directory
cd vapoursynth

# Start the shell (this line must always be last)
exec /bin/bash
