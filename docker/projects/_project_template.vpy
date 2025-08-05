import vapoursynth as vs
core = vs.core

#core.num_threads = 24
core.max_cache_size = 15000









video_path = "/workspace/vapoursynth/projects/video.mkv"
clip = core.bs.VideoSource(source=video_path, cachemode=3)




clip.set_output(0)





































