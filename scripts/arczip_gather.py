# coding: utf-8

import os
import shutil
import arczip
import re

def copy_tda4_libs(save_dir):
    algo_module_lst = [
        'ascc', 'calibinner', 'encode', 'fusion',
        'ir_night_contour', 'ir_night_vpd', 'ir_night_vpt', 'msind',
        'toy_core',
        'toy_calib3d',
        'toy_imgproc',
        #'toy_fourcc',
        'toy_shape_analysis',
        #'toy_imageio',
        'undistort_points'
    ]

    if (not os.path.exists(save_dir)):
        os.mkdir(save_dir)

    for name in algo_module_lst:
        lib_dir = '{:s}/lib/linux_arm64_tda4'.format(name)
        for item in os.listdir(lib_dir):
            if (item.endswith('.a')):
                lib_src_path = os.path.join(lib_dir, item)
                lib_dst_path = os.path.join(save_dir, item)
                print('copy {:s} to {:s}'.format(lib_src_path, lib_dst_path))
                shutil.copy(lib_src_path, lib_dst_path)
    print("===\nCopy libs done\n\n")

def containVersion(word):
    versionPattern = r"_\d{1,3}.\d{1,3}.\d{1,10}.\d{1,5}"
    match = re.search(versionPattern, word)
    if (match is not None):
        return True
    return False

def print_module_version(lib_pth):
    for word_bytes in arczip.strings(lib_pth):
        word = word_bytes.decode()
        if (word.startswith('ArcSoft') and containVersion(word)):
            print(word)
        elif (word.startswith('arcsoft') and containVersion(word)):
            print(word)

# This is an example, it print single library's version
def print_ascc():
    lib_pth = 'tda4_libs/libarcsoft_adas_ascc.a'
    print_module_version(lib_pth)

class ToyVisionVerion(object):
    def __init__(self, version_str):
        items = version_str.split('-')
        self.major, self.minor, self.patch = items[2].split('.')
        self.githash = items[-1]
        self.version_str = version_str
    def __str__(self):
        return self.version_str

def get_toy_core_version(lib_pth):
    for word_bytes in arczip.strings(lib_pth):
        word = word_bytes.decode()
        if (word.startswith('toy-vision-')):
            return ToyVisionVerion(word)

def auto_print_lib_version(lib_dir):
    """
    This function automatically scan the given directory, for all .a libraries it search and print version string
    Which is quite useful for SVN commit message / AutoBuild update point.
    """
    common_modules = []
    toycv_modules = []
    for item in os.listdir(lib_dir):
        if (item.endswith('.a') and (item.startswith('libarcsoft_'))):
            common_modules.append(item)
        elif (item.startswith('libtoy_') and (item.endswith('.a'))):
            toycv_modules.append(item)
    
    print('Dependency list:')
    for item in common_modules:
        lib_pth = lib_dir + "/" + item
        print_module_version(lib_pth)
    
    tv_ver = get_toy_core_version(lib_dir + "/" + "libtoy_core.a")
    print("ToyVision", tv_ver)
    for item in toycv_modules:
        print("    " + item + " {:}.{:}.{:}".format(tv_ver.major, tv_ver.minor, tv_ver.patch))


if __name__ == '__main__':
    # print_ascc()

    tda4_lib_dir = 'tda4_libs'
    copy_tda4_libs(tda4_lib_dir)
    auto_print_lib_version(tda4_lib_dir)