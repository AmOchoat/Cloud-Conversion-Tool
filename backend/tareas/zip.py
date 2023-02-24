import zipfile
import os
import sys

def compress(filename, zipname, new_path):
    zfile = zipfile.ZipFile(new_path + '/' + zipname, 'w')
    zfile.write(filename, compress_type = zipfile.ZIP_DEFLATED)
    zfile.close()
