
#############################################
# IMPORTS AND PLUGINS
#############################################

import sys
import vapoursynth as vs
import functools
import random
import vs_liif
import vs_align
import vs_colorfix
import numpy as np
import cv2
import os
import warnings
from vs_iqa import vs_iqa

core = vs.core




#############################################
# SETTINGS AND PATHS
#############################################

# Output paths
save_dataset   = True # If the dataset should be saved to disk, or not.
output_path    = "path/to/save_folder"
LR_subfolder   = "LR"
HR_subfolder   = "HR"
save_interval  = 10 # How many frames to save. 1 saves every frame, 10 saves every 10th frame.

# Input paths
source_path_LR = "path/to/LR_video.mkv"
source_path_HR = "path/to/HR_video.mkv"

# Input color matrix
LR_matrix_in_s = "709" # 709 for new sources like bluray and web, 470bg for older sources like dvd.
HR_matrix_in_s = "709" # 709 for new sources like bluray and web, 470bg for older sources like dvd.

# Input frame rate (only needed if they differ)
LR_fpsnum      = None  # Numerator for LR video.
LR_fpsden      = None  # Denominator for LR video.
HR_fpsnum      = None  # Numerator for HR video.
HR_fpsden      = None  # Denominator for HR video.

# Scale
scale_factor   = 2     # How many times is HR larger than LR.
resize_HR      = True  # If HR is not exactly a multiple of LR, True resizes HR to get to the desired scale factor, False resizes LR to get to desired scale factor.
liif_resize    = False # Uses liif AI resizing to get to the desired scale factor.

# Crop (Use this to make the visible area of both sources match as close as possible and to crop black borders. Else the temporal alignment will not work correctly.)
LR_crop_left   = 0
LR_crop_right  = 0
LR_crop_top    = 0
LR_crop_bottom = 0

HR_crop_left   = 0
HR_crop_right  = 0
HR_crop_top    = 0
HR_crop_bottom = 0

# Trims
LR_trim        = 0     # Cuts this number of frames at the beginning.
HR_trim        = 0     # Cuts this number of frames at the beginning.

# Temporal alignment settings
temporal_align      = True       # Whether to synchronize both clips. First frame needs to match, which can be done with the trims above.
temporal_radius     = 20         # Determines how many frames to search forwards and backwards for a match. Higher is slower.
diff_threshold      = 0.7        # Threshold at which LR and HR differ so much, they should not be saved. Higher means pairs can be very different, lower means pairs should be less different. Range 0-1.
batch_size          = None       # Controls VRAM usage for temporal alignment. A value lower than tr will reduce VRAM usage, but is a bit slower.

# Spatial alignment settings
spatial_align       = True       # Whether to align the individual frames in space by shifting and warping.

# Color match settings
color_match         = True       # Colors will be transfered from HR to LR (HR stays the same, LR changes colors).
change_HR           = True       # Transfers colors from LR to HR instead (LR stays the same, HR changes colors).

# Iqa settings
HR_iqa              = False      # Uses image quality assessment to filter out low quality frames.
HR_iqa_metric       = 'hyperiqa' # More metrics can be found in the "NR Method" table here: https://github.com/chaofengc/IQA-PyTorch/blob/main/docs/ModelCard.md
HR_iqa_threshold    = 0.2        # If quality is lower/higher than this value, image will not be saved. Range 0-1 for hyperiqa, can be different with others.
HR_iqa_mode         = 'lower'    # Lower means frames below threshold will be filtered out (only best are saved), Higher means frames above threshold will be filtered out (only worst are saved).
LR_iqa              = False
LR_iqa_metric       = 'hyperiqa' # More metrics can be found in the "NR Method" table here: https://github.com/chaofengc/IQA-PyTorch/blob/main/docs/ModelCard.md
LR_iqa_threshold    = 0.7        # If quality is lower/higher than this value, image will not be saved. Range 0-1 for hyperiqa, can be different with others.
LR_iqa_mode         = 'higher'   # Lower means frames below threshold will be filtered out (only best are saved), higher means frames above threshold will be filtered out (only worst are saved).

# Additional processing
chroma_bleed        = False      # This will blur the chroma channels to create bleed.
bleed_radius        = (1, 20)    # Range of bleed radius.
bleed_intensity     = (10, 100)  # Range of bleed intensity. Possible values 0-100.

chroma_shift        = False      # This will shift the chroma channels down; use flip and rotate to change direction.
shift_amount        = (0.1, 3)   # Range of shift amount. One decimal place possible.
shift_intensity     = (100, 100) # Range of bleed intensity. possible values 0-100.
flip_vertical       = (0, 1)     # Changes the direction of the chroma shift vertically, 0 and 1 possible.
rotate_90           = (0, 1)     # Changes the direction of the chroma shift horizontally, 0 and 1 possible.

banding             = False      # This will create banding or low bit depth artifacts.
banding_stregth     = (0, 16)    # Range of depth reduction, values 0 to 127.

# Final crop (not required, but recommended because the alignment sometimes creates artifacts near the edges)
final_crop_left   = 10
final_crop_right  = 10
final_crop_top    = 10
final_crop_bottom = 10




#############################################
# PREPROCESS
#############################################

# load sources
LR = core.bs.VideoSource(source=source_path_LR)
HR = core.bs.VideoSource(source=source_path_HR)

# set frameprop for saving
LR = core.std.SetFrameProp(LR, prop="save_to_file", data=["true"])
HR = core.std.SetFrameProp(HR, prop="save_to_file", data=["true"])

# time offsets
LR = core.std.Trim(LR, first=LR_trim)
HR = core.std.Trim(HR, first=HR_trim)

# crop and resize
LR = core.resize.Bilinear(LR, format = vs.RGBS, matrix_in_s=LR_matrix_in_s, range_s='full')
HR = core.resize.Bilinear(HR, format = vs.RGBS, matrix_in_s=HR_matrix_in_s, range_s='full')

LR = core.std.Crop(LR, left=LR_crop_left, right=LR_crop_right, top=LR_crop_top, bottom=LR_crop_bottom)
HR = core.std.Crop(HR, left=HR_crop_left, right=HR_crop_right, top=HR_crop_top, bottom=HR_crop_bottom)




#############################################
# DENOISE
#############################################

#if HR_denoise:
#    HR = core.resize.Bilinear(HR, format = vs.YUV444P16, matrix_s="709", range_in_s='full', range_s='full')
#    # placeholder space to denoise HR clip
#    HR = core.resize.Bilinear(HR, format = vs.RGBS, matrix_in_s=709, range_in_s='full', range_s='full')

#if LR_denoise:
#    LR = core.resize.Bilinear(LR, format = vs.YUV444P16, matrix_s="709", range_in_s='full', range_s='full')
#    # placeholder space to denoise LR clip
#    LR = core.resize.Bilinear(LR, format = vs.RGBS, matrix_in_s=709, range_in_s='full', range_s='full')




#############################################
# TEMPORAL ALIGNMENT
#############################################

black = core.std.BlankClip(LR, length=HR.num_frames, format=vs.RGB24, color=[0, 0, 0])
fallback_clip = core.resize.Point(black, format=LR.format, width=LR.width, height=LR.height, range_in_s='full', range_s='full')
fallback_clip = core.std.SetFrameProp(fallback_clip, prop="save_to_file", data=["false"])

# preprocessing LR for temporal alignment, crop, resize
LR_preprocess = core.resize.Bilinear(LR, format = vs.YUV444P16, matrix_s="709", width=480, height=360, range_in_s='full', range_s='full')
LR_preprocess = core.std.Crop(LR_preprocess, left=2, right=2, top=2, bottom=2)

# preprocessing HR for temporal alignment, crop, resize
HR_preprocess = core.resize.Bilinear(HR, format = vs.YUV444P16, matrix_s="709", width=480, height=360, range_in_s='full', range_s='full')
HR_preprocess = core.std.Crop(HR_preprocess, left=2, right=2, top=2, bottom=2)

# temporal alignment
if temporal_align:
    LR = vs_align.temporal(LR_preprocess, HR_preprocess, LR, tr=temporal_radius, fallback=fallback_clip, thresh=diff_threshold, precision=3, clip_num=LR_fpsnum, clip_den=LR_fpsden, ref_num=HR_fpsnum, ref_den=HR_fpsden, batch_size=batch_size, device="cuda", debug=False)

# set save interval
if save_interval > 1:
    LR = core.std.SelectEvery(LR, cycle=save_interval, offsets=0)
    HR = core.std.SelectEvery(HR, cycle=save_interval, offsets=0)
  



#############################################
# SPATIAL ALIGNMENT
#############################################

# resize HR to LR's size
HR_for_align = core.resize.Bicubic(HR, width=LR.width, height=LR.height)

# spatial alignment
if spatial_align:
    LR = vs_align.spatial(LR, HR_for_align, precision=3, wide_search=True, lq_input=True, device="cuda")

# resize LR to HR/scale_factor
if resize_HR:
    target_width = LR.width * scale_factor
    target_height = LR.height * scale_factor
    if HR.width != target_width or HR.height != target_height:
        if liif_resize:
            HR = vs_liif.resize(HR, width=target_width, height=target_height, device="cuda")
        else:
            HR = core.resize.Bicubic(HR, width=target_width, height=target_height)
else:
    target_width = HR.width / scale_factor
    target_height = HR.height / scale_factor
    if LR.width != target_width or LR.height != target_height:
        if liif_resize:
            LR = vs_liif.resize(LR, width=target_width, height=target_height, device="cuda")
        else:
            LR = core.resize.Bicubic(LR, width=target_width, height=target_height)



#############################################
# COLOR MATCHING
#############################################

if color_match:
    if change_HR:
        HR = vs_colorfix.wavelet(HR, LR, device="cuda")
    else:
        LR = vs_colorfix.wavelet(LR, HR, device="cuda")




#############################################
# IQA
#############################################

if HR_iqa:
    fallback_clip_HR = core.resize.Point(fallback_clip, format=HR.format, width=HR.width, height=HR.height, range_in_s='full', range_s='full')
    HR = vs_iqa(HR, fallback=fallback_clip_HR, thresh=HR_iqa_threshold, thresh_mode=HR_iqa_mode, metric=HR_iqa_metric , device='cuda', debug=False)

if LR_iqa:
    fallback_clip_LR = core.resize.Point(fallback_clip, format=LR.format, width=LR.width, height=LR.height, range_in_s='full', range_s='full')
    LR = vs_iqa(LR, fallback=fallback_clip_LR, thresh=LR_iqa_threshold, thresh_mode=LR_iqa_mode, metric=LR_iqa_metric , device='cuda', debug=False)




#############################################
# ADDITIONAL DEGREDATIONS
#############################################

LR = core.resize.Bilinear(LR, format = vs.YUV444P16, matrix_s="709", range_in_s='full', range_s='full')

# chroma bleed
def chroma_bleed_func(n, clip):
    rand_bleed_radius = random.randint(*bleed_radius)
    rand_bleed_intensity = random.randint(*bleed_intensity)
    bleed = core.resize.Bilinear(clip, width=clip.width*4, height=clip.height*4)
    bleed = core.std.BoxBlur(bleed, hradius=rand_bleed_radius, hpasses=3, vradius=rand_bleed_radius, vpasses=3)
    bleed = core.resize.Bilinear(bleed, width=bleed.width/4, height=bleed.height/4)
    bleed = core.std.AverageFrames(clips=[bleed, clip], weights=[rand_bleed_intensity, 100-rand_bleed_intensity])
    return core.std.ShufflePlanes(clips=[clip, bleed, bleed], planes=[0, 1, 2], colorfamily=vs.YUV)
if chroma_bleed:
    LR = core.std.FrameEval(LR, functools.partial(chroma_bleed_func, clip=LR))

# chroma shift
def chroma_shift_func(n, clip):
    rand_shift_amount = random.randint(int(shift_amount[0] * 10), int(shift_amount[1] * 10))
    rand_flip_vertical = random.randint(*flip_vertical)
    rand_rotate_90 = random.randint(*rotate_90)
    rand_shift_intensity = random.randint(*shift_intensity)
    
    clip = core.std.Transpose(clip) if rand_rotate_90 else clip
    clip = core.std.FlipVertical(clip) if rand_flip_vertical else clip
    shifted_chroma = core.resize.Point(clip, clip.width, clip.height*10)
    shifted_chroma = core.std.Crop(shifted_chroma, top=rand_shift_amount, bottom=0, left=0, right=0)
    shifted_chroma = core.std.AddBorders(shifted_chroma, top=0, bottom=rand_shift_amount, left=0, right=0)
    shifted_chroma = core.resize.Bicubic(shifted_chroma, clip.width, clip.height)
    shifted_chroma = core.std.AverageFrames(clips=[shifted_chroma, clip], weights=[rand_shift_intensity, 100-rand_shift_intensity])
    clip = core.std.ShufflePlanes([clip, shifted_chroma, shifted_chroma], [0, 1, 2], vs.YUV)
    clip = core.std.FlipVertical(clip) if rand_flip_vertical else clip
    clip = core.std.Transpose(clip) if rand_rotate_90 else clip
    return clip
if chroma_shift:
    LR = core.std.FrameEval(LR, functools.partial(chroma_shift_func, clip=LR))

# banding
def banding_func(n, clip):
    rand_banding_stregth = random.randint(*banding_stregth)
    if rand_banding_stregth == 0:
        return clip
    else:
        clip = core.resize.Bilinear(clip, format = vs.YUV444P8, range_in_s='full', range_s='full')
        clip = core.std.Levels(clip, min_in=0, min_out=rand_banding_stregth, max_in=255, max_out=255-rand_banding_stregth)
        clip = core.tbilateral.TBilateral(clip, diameter=39, sdev=100000, idev=1, cs=1, d2=False, kerns=2, kerni=2, restype=0)
        clip = core.tbilateral.TBilateral(clip, diameter=19, sdev=100000, idev=1, cs=1, d2=False, kerns=2, kerni=2, restype=0)
        clip = core.tbilateral.TBilateral(clip, diameter=7, sdev=100000, idev=1, cs=1, d2=False, kerns=2, kerni=2, restype=0)
        clip = core.std.Levels(clip, min_in=rand_banding_stregth, min_out=0, max_in=255-rand_banding_stregth, max_out=255)
        return core.resize.Bilinear(clip, format = vs.YUV444P16, range_in_s='full', range_s='full')
if banding:
    LR = core.std.FrameEval(LR, functools.partial(banding_func, clip=LR))

# put additional degredations here if needed




#############################################
# WRITE DATASET TO DISK
#############################################

LR = core.std.Crop(LR, left=final_crop_left, right=final_crop_right, top=final_crop_top, bottom=final_crop_bottom)
HR = core.std.Crop(HR, left=final_crop_left*scale_factor, right=final_crop_right*scale_factor, top=final_crop_top*scale_factor, bottom=final_crop_bottom*scale_factor)

LR = core.resize.Bilinear(LR, format=vs.RGB24, matrix_in_s="709", range_in_s='full', range_s='full')
HR = core.resize.Bilinear(HR, format=vs.RGB24, matrix_in_s="709", range_in_s='full', range_s='full')

def write_frame(frame: vs.VideoFrame, filename: str) -> None:
    array = np.dstack([np.asarray(frame[p]) for p in range(frame.format.num_planes)])
    array = array[:, :, ::-1]
    array = array.astype(np.uint8)
    cv2.imwrite(filename, array)

def save_to_disk(LR, HR, prop_name, save_folder, lr_subfolder, hr_subfolder, save=True):
    if save:
        # use the specified subfolder names for LR and HR
        LR_folder = os.path.join(save_folder, lr_subfolder)
        HR_folder = os.path.join(save_folder, hr_subfolder)
        os.makedirs(LR_folder, exist_ok=True)
        os.makedirs(HR_folder, exist_ok=True)
        
        # check if folders are empty
        lr_folder_empty = not os.listdir(LR_folder)
        hr_folder_empty = not os.listdir(HR_folder)
    
        if not lr_folder_empty:
            warnings.warn(f"WARNING: Folder '{LR_folder}' exists and is not empty. Images will not be saved to avoid overwriting.")
        if not hr_folder_empty:
            warnings.warn(f"WARNING: Folder '{HR_folder}' exists and is not empty. Images will not be saved to avoid overwriting.")

    def _get_frame_prop(n, f):
        lr_prop_value = f.props.get(prop_name, None)
        lr_iqa_score = f.props.get('vs_iqa_score', None)
        
        hr_frame = HR.get_frame(n)
        hr_prop_value = hr_frame.props.get(prop_name, None)
        hr_iqa_score = hr_frame.props.get('vs_iqa_score', None)
        
        
        # check if both frame props exist and are "true", then save the current frames of both clips
        if (save and 
            lr_prop_value is not None and lr_prop_value == "true" and
            hr_prop_value is not None and hr_prop_value == "true"):
            
            lr_filename = os.path.join(LR_folder, f"frame_{n}.png")
            if lr_folder_empty:
                write_frame(LR.get_frame(n), lr_filename)
                
            hr_filename = os.path.join(HR_folder, f"frame_{n}.png")
            if hr_folder_empty:
                write_frame(hr_frame, hr_filename)
        
        # overlay frame props on the LR frame
        overlay_text = (
            f"Images will only be saved to\ndisk if BOTH are true.\n"
            f"\n"
            f"LR IQA score: {lr_iqa_score if lr_iqa_score is not None else 'None'}\n"
            f"HR IQA score: {hr_iqa_score if hr_iqa_score is not None else 'None'}\n"
            f"\n"
            f"LR {prop_name}: {lr_prop_value if lr_prop_value else 'None'}\n"
            f"HR {prop_name}: {hr_prop_value if hr_prop_value else 'None'}\n"
        )
        return core.text.Text(clip=LR, text=overlay_text, alignment=6)

    return core.std.FrameEval(LR, eval=_get_frame_prop, prop_src=[LR])

LR = save_to_disk(LR, HR, "save_to_file", os.path.abspath(output_path), LR_subfolder, HR_subfolder, save=save_dataset)




#############################################
# EXPORT
#############################################

LR = core.resize.Point(LR, format=vs.YUV420P8, matrix_s="709", range_in_s='full', range_s='limited')
LR.set_output(0)
