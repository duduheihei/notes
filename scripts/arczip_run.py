# coding: utf-8

import arczip
import platform

# \\hz-delivery\ImageTECH\2022Q4\22606\22606-3\Related_Project
if (platform.system().lower() == "windows"):
    prefix = "D:/work/adas-framework/byd-ir-night-raw-pkgs/"
    #prefix = "C:/Users/zz/work/adas-framework/byd-ir-night-raw-pkgs/"
elif (platform.system().lower() == "linux"):
    prefix = "D:/work/adas-framework/byd-ir-night-raw-pkgs/"


def parse_ir_night_vpd():
    zippath_lst = [
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.21623.16_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03302023_AUTOBUILD_18.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.30302.16_VS2017_X64_STATIC_FOR_ARCSOFT_03302023_AUTOBUILD_19.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.30302.16_VS2017_X64_STATIC_FOR_ARCSOFT_03302023_AUTOBUILD_20_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.30302.17_VS2017_X64_STATIC_FOR_ARCSOFT_04032023_AUTOBUILD_22.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.30302.17_VS2017_X64_STATIC_FOR_ARCSOFT_04032023_AUTOBUILD_23_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.21623.17_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_21.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.303020.19_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_30_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.303020.19_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_29.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.21623.19_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_28.zip",
        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.21623.19_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_28.zip",
        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.303020.19_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_29.zip",
        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPD_2.0.303020.19_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_30_DEBUG.zip",
    ]
    temp_dir = "temp/ir_night_vpd"
    pkg_dir = "ir_night_vpd"
    pkg_name = "arcsoft_adas_ir_night_vpd"
    require_lst = ["mpbase"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_ir_night_vpt():
    zippath_lst = [
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.21623.11_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03302023_AUTOBUILD_11.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.30302.11_VS2017_X64_STATIC_FOR_ARCSOFT_03302023_AUTOBUILD_12.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.30302.11_VS2017_X64_STATIC_FOR_ARCSOFT_03302023_AUTOBUILD_13_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.21623.12_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_14.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.30302.12_VS2017_X64_STATIC_FOR_ARCSOFT_04032023_AUTOBUILD_15.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.30302.12_VS2017_X64_STATIC_FOR_ARCSOFT_04032023_AUTOBUILD_16_DEBUG.zip",

        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.303020.14_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_19_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.303020.14_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_18.zip",
        # prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.21623.14_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_17.zip",

        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.21623.14_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_17.zip",
        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.303020.14_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_18.zip",
        prefix + "ARCSOFT_ADAS_IR_NIGHT_VPT_2.0.303020.14_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_19_DEBUG.zip",
    ]
    temp_dir = "temp/ir_night_vpt"
    pkg_dir = "ir_night_vpt"
    pkg_name = "arcsoft_adas_ir_night_vpt"
    require_lst = ["mpbase"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()

def parse_ir_night_contour_v1():
    zippath_lst = [
        prefix + "ARCSOFT_ADAS_IR_NIGHT_CONTOUR_2.0.0.2_TDA4_FOR_ARCSOFT_03302023.zip"
    ]
    temp_dir = "temp/ir_night_contour"
    pkg_dir = "ir_night_contour"
    pkg_name = "arcsoft_adas_ir_night_contour"
    require_lst = ["mpbase", "arcnn", "toy_shape_analysis", "toy_imgproc", "toy_core"]

    vs_platform_arch = arczip.get_vs_platform_arch(zippath_lst)
    arczip.unzip_package_zips(zippath_lst, temp_dir)
    candidate_dirs = arczip.get_candidate_dirs(temp_dir)
    arczip.copy_inc_dir(candidate_dirs[0], pkg_dir)
    arczip.copy_windows_x64_lib_dir(candidate_dirs, pkg_dir, keyword="TDA4") #!! 就一个 zip, windows 库也放在这里了
    arczip.copy_tda4_lib_dir(candidate_dirs, pkg_dir, keyword="TDA4") #!! 就一个 zip, tda4 名字也只有 TDA4 字段
    arczip.write_cmakelist(pkg_dir, pkg_name, require_lst, vs_platform_arch)

def parse_ir_night_contour():
    zippath_lst = [
        # prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.30302.3_VS2017_X64_STATIC_FOR_ARCSOFT_04012023_AUTOBUILD_5_DEBUG.zip",
        # prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.30302.3_VS2017_X64_STATIC_FOR_ARCSOFT_04012023_AUTOBUILD_4.zip",
        # prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.21623.3_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04012023_AUTOBUILD_3.zip"
        prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.303020.4_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_8_DEBUG.zip",
        prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.21623.4_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_6.zip",
        prefix + "ARCSOFT_IR_NIGHT_CONTOUR_2.0.303020.4_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_7.zip",
    ]
    temp_dir = "temp/ir_night_contour"
    pkg_dir = "ir_night_contour"
    pkg_name = "arcsoft_adas_ir_night_contour"
    require_lst = ["mpbase", "arcnn", "toy_shape_analysis", "toy_imgproc", "toy_core"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()

def parse_encode():
    zippath_lst = [
        # prefix + "ARCSOFT_ADAS_ENCODE_1.3.30302.23005_VS2017_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_3_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_ENCODE_1.3.30302.23005_VS2017_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_2.zip",
        # prefix + "ARCSOFT_ADAS_ENCODE_1.3.21623.23005_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_13.zip",
        prefix + "ARCSOFT_ADAS_ENCODE_1.3.30302.23007_VS2017_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_9.zip",
        prefix + "ARCSOFT_ADAS_ENCODE_1.3.30302.23007_VS2017_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_8_DEBUG.zip",
        prefix + "ARCSOFT_ADAS_ENCODE_1.3.21623.23007_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04072023_AUTOBUILD_17.zip",
    ]
    temp_dir = "temp/encode"
    pkg_dir = "encode"
    pkg_name = "arcsoft_adas_encode"
    require_lst = ["protobuf"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_ascc():
    zippath_lst = [
        # prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_56_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_57.zip",
        # prefix + "ARCSOFT_ADAS_ASCC_2.0.21623.1_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_34.zip",
        prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_66_DEBUG.zip",
        prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_65.zip",
        prefix + "ARCSOFT_ADAS_ASCC_2.0.21623.1_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04182023_AUTOBUILD_38.zip",
    ]
    temp_dir = "temp/ascc"
    pkg_dir = "ascc"
    pkg_name = "arcsoft_adas_ascc"
    require_lst = ["mpbase", "arcnn"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_calibinner():
    zippath_lst = [
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_56_DEBUG.zip",
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_57.zip",
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.21623.1_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_34.zip",

        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.21623.20_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_163.zip",
        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.20_VS2017_X64_STATIC_FOR_ARCSOFT_04032023_AUTOBUILD_16_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.20_VS2017_X64_STATIC_FOR_ARCSOFT_04042023_AUTOBUILD_18.zip",

        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.21623.20_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_163.zip", # TODO: fix me
        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.21_VS2017_X64_STATIC_FOR_ARCSOFT_04102023_AUTOBUILD_23.zip",
        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.21_VS2017_X64_STATIC_FOR_ARCSOFT_04102023_AUTOBUILD_22_DEBUG.zip",

        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.22_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_26_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.22_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_25.zip",

        prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.22_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_28_DEBUG.zip",
        prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.30302.22_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_27.zip",
        prefix + "ARCSOFT_ADAS_CALIBINNER_1.0.21623.22_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04182023_AUTOBUILD_170.zip"
    ]
    temp_dir = "temp/calibinner"
    pkg_dir = "calibinner"
    pkg_name = "arcsoft_adas_calibinner"
    require_lst = ["mpbase", "toy_calib3d", "arcsoft_undistort_points"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_msind():
    zippath_lst = [
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_56_DEBUG.zip",
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_57.zip",
        #prefix + "ARCSOFT_ADAS_ASCC_2.0.21623.1_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_34.zip",

        # prefix + "ARCSOFT_ADAS_MSIND_1.3.21623.23022_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_71.zip",
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23022_VS2017_X64_STATIC_FOR_ARCSOFT_04042023_AUTOBUILD_18.zip",
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23022_VS2017_X64_STATIC_FOR_ARCSOFT_04042023_AUTOBUILD_17_DEBUG.zip",

        # prefix + "ARCSOFT_ADAS_MSIND_1.3.21623.23022_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04032023_AUTOBUILD_71.zip", # TODO: fix me
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23023_VS2017_X64_STATIC_FOR_ARCSOFT_04102023_AUTOBUILD_24_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23023_VS2017_X64_STATIC_FOR_ARCSOFT_04102023_AUTOBUILD_25.zip",

        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23024_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_27_DEBUG.zip",
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23024_VS2017_X64_STATIC_FOR_ARCSOFT_04172023_AUTOBUILD_26.zip",
        # prefix + "ARCSOFT_ADAS_MSIND_1.3.21623.23024_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04172023_AUTOBUILD_83.zip",

        prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23024_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_29.zip",
        prefix + "ARCSOFT_ADAS_MSIND_1.3.30302.23024_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_28_DEBUG.zip",
        prefix + "ARCSOFT_ADAS_MSIND_1.3.21623.23024_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04182023_AUTOBUILD_86.zip",
    ]
    temp_dir = "temp/msind"
    pkg_dir = "msind"
    pkg_name = "arcsoft_adas_msind"
    require_lst = ["mpbase", "arcsoft_adas_calibinner"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_undistort_points():
    zippath_lst = [
        prefix + "ARCSOFT_UNDISTORT_POINTS_0.0.30302.6_VS2017_X64_SHARED_FOR_ARCSOFT_04062023_AUTOBUILD_18.zip",
        prefix + "ARCSOFT_UNDISTORT_POINTS_0.0.30302.6_VS2017_X64_SHARED_FOR_ARCSOFT_04062023_AUTOBUILD_20_DEBUG.zip",
        prefix + "ARCSOFT_UNDISTORT_POINTS_0.0.21623.6_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04042023_AUTOBUILD_42.zip",
    ]
    temp_dir = "temp/undistort_points"
    pkg_dir = "undistort_points"
    pkg_name = "arcsoft_undistort_points"
    require_lst = ["mpbase"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_decode():
    zippath_lst = [
        prefix + "ARCSOFT_ADAS_DECODE_1.3.21623.23003_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04072023_AUTOBUILD_5.zip",
        prefix + "ARCSOFT_ADAS_DECODE_1.3.30402.23003_VS2019_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_1.zip",
        prefix + "ARCSOFT_ADAS_DECODE_1.3.30402.23003_VS2019_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_2_DEBUG.zip",
    ]
    temp_dir = "temp/decode"
    pkg_dir = "decode"
    pkg_name = "arcsoft_adas_decode"
    require_lst = ["protobuf"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


def parse_fusion():
    zippath_lst = [
        # prefix + "ARCSOFT_ADAS_DECODE_1.3.21623.23003_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04072023_AUTOBUILD_5.zip",
        # prefix + "ARCSOFT_ADAS_DECODE_1.3.30402.23003_VS2019_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_1.zip",
        # prefix + "ARCSOFT_ADAS_DECODE_1.3.30402.23003_VS2019_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_2_DEBUG.zip",

        prefix + "ARCSOFT_ADAS_FUSION_3.0.21623.0_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04182023_AUTOBUILD_6.zip",
        prefix + "ARCSOFT_ADAS_FUSION_3.0.30302.0_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_5_DEBUG.zip",
        prefix + "ARCSOFT_ADAS_FUSION_3.0.30302.0_VS2017_X64_STATIC_FOR_ARCSOFT_04182023_AUTOBUILD_6.zip",
    ]
    temp_dir = "temp/fusion"
    pkg_dir = "fusion"
    pkg_name = "arcsoft_adas_fusion"
    require_lst = ["mpbase"]
    zipper = arczip.AutoUnzipper(zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst)
    zipper.run()


if __name__ == '__main__':
    # parse_ir_night_vpd() # ok
    # parse_ir_night_vpt() # ok
    # parse_ir_night_contour() # ok

    # parse_encode() # ok

    # parse_ascc() # ok

    # toycv_version = "1.3.2"
    # # #toycv_version = "1.1.32"
    # arczip.parse_toy_core(toycv_version, prefix)
    # arczip.parse_toy_imgproc(toycv_version, prefix)
    # arczip.parse_toy_fourcc(toycv_version, prefix)
    # arczip.parse_toy_shape_analysis(toycv_version, prefix)
    # arczip.parse_toy_calib3d(toycv_version, prefix)
    # arczip.parse_toy_imageio(toycv_version, prefix)

    parse_undistort_points() # ok

    parse_calibinner() #
    parse_msind() #
    parse_fusion() #