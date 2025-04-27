# debug_path_check.py
import os, realtime_slider

p = os.path.join(os.path.dirname(realtime_slider.__file__),
                 "frontend", "dist")
print("dist への絶対パス:", p)
print("index.html 存在:", os.path.exists(os.path.join(p, "index.html")))