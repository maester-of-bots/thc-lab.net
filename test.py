import os

baseDir = '/home/thc'

# Look at all files / folders in the base directory
for subdir in os.listdir(baseDir):
    if "." in subdir:
        pass
    else:
        subfiles = os.listdir(os.path.join(baseDir,subdir))
        for subfile in subfiles:
            if subfile == "readme.txt":
                os.rename(os.path.join(baseDir,subdir,subfile),os.path.join(baseDir,subdir,"fuckyou.txt"))
            elif "." in subfile:
                pass
            else:
                try:
                    for subsubfile in os.path.join(baseDir,subfile):
                        if subsubfile == "readme.txt":
                            os.rename(os.path.join(baseDir,subdir,subsubfile), os.path.join(baseDir,subdir,"fuckyou.txt"))
                except:
                    pass