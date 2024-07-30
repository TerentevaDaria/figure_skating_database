import sys, os, subprocess
import glob

f = os.getenv("GENERATE")
if f != "True":
    exit(0)

files = []
for i in glob.glob("/data_generation/*.*.*.py"):
    v = i.split('/')[-1].split('+')[0].split('.')
    files.append((int(v[0]), int(v[1]), int(v[2]), i))
files.sort()

v = os.getenv("VERSION")
for i in files:
    if v is None:
        os.system(f"python -u {i[3]}")
    else:
        last_major = v.split('.')[0]
        last_minor = v.split('.')[1]
        last_patch = v.split('.')[2]
        if i[0] < last_major or i[0] == last_major and i[1] < last_patch or i[0] == last_major and i[1] == last_patch and i[2] <= last_patch:
            os.system(f"python -u {i[3]}")
