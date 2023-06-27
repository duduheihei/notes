# coding: utf-8
#
#----------------------------------------------------------------------
# Author: Zhuo Zhang(imzhuo@foxmail.com)
# Create: 2023-03-30 00:00:00
# Last modified: 2023-04-18 23:32:24
#----------------------------------------------------------------------
# Description:
# arczip: a collection of functionality for autobuild zip package management
# 目前有三大功能:
# 1. 解析公司 autobuild 生成的 .zip 包名称， 得到结构化的结果 (DeliveryPackageNameParser)
# 2. 解压 autobuild .zip 包到统一的目录， 并自动生成 CMakeLists.txt, 用于 add_subdirectory()方式使用
# 3. 提供 strings 命令的 Python 实现，用于打印 .a 库文件中的 SDK 版本号字符串

import zipfile
import os
import shutil
import re
import unittest
from mytest import MyTestRunner

#--------------------------------------------------------------------------------
# Delivery Zipfile Parsing / Generation
#--------------------------------------------------------------------------------

# 解析公司递交包格式 https://confluence.arcsoft.com.cn/pages/viewpage.action?pageId=7382099
class DeliveryPackageNameParser(object):
    def __init__(self, zipname = None):
        self.zipname = zipname

    #----------------------------------------------------------------------
    # level0  global settings
    #----------------------------------------------------------------------
    def getSupportedBuildTypes(self):
        return ['STATIC', 'SHARED']


    #----------------------------------------------------------------------
    # level1 parsing: zipname = p1 p2 p3 p4 p5 .zip
    #----------------------------------------------------------------------
    def parseVersion(self, zipname):
        pattern = r"_\d{1,3}.\d{1,3}.\d{1,10}.\d{1,5}_"
        return re.search(pattern, zipname)

    def parseBuildDate(self, zipname):
        yearPattern = "20[0-9][0-9]"
        monthPattern = "((0[1-9])|(1[0-2]))" # TODO:
        dayPattern = "(([0][1-9]|[1-2][0-9]|3[0-1]))"
        pattern1 = "_{:s}{:s}{:s}_".format(yearPattern, monthPattern, dayPattern) # e.g. 20160613

        pattern2 = "_{:s}{:s}{:s}(_|.)".format(monthPattern, dayPattern, yearPattern) # e.g. 03222023.zip  03222023_Debug.zip

        pattern = "(({:s})|({:s}))".format(pattern1, pattern2)
        return re.search(pattern, zipname)

    def getP1(self, zipname):
        pos = zipname.find('ARCSOFT_')
        return zipname[0:pos]

    def getP2(self, zipname):
        versionMatch = self.parseVersion(zipname)
        startPos = zipname.find('ARCSOFT_')
        endPos = versionMatch.end()
        p2 = zipname[startPos:endPos]
        return p2

    def getP3(self, zipname):
        versionMatch = self.parseVersion(zipname)
        startPos = versionMatch.end()

        buildDateMatch = self.parseBuildDate(zipname)
        endPos = buildDateMatch.start()

        p3 = zipname[startPos:endPos]
        return p3

    def getP4(self, zipname):
        match = self.parseBuildDate(zipname)
        startPos = match.start()
        endPos = match.end()
        p4 = zipname[startPos:endPos]
        return p4

    def getP5(self, zipname):
        match = self.parseBuildDate(zipname)
        startPos = match.end()
        p5 = zipname[startPos:-4]
        return p5

    #----------------------------------------------------------------------
    # level2 parsing: parse each of p1, p2, p3, p4
    #----------------------------------------------------------------------

    #----------------------------------------------------------------------
    # parse p1
    #----------------------------------------------------------------------
    def parseProjectID(self, zipname):
        p1 = self.getP1(zipname)
        pattern = r"^\d{1,5}_"
        return re.search(pattern, p1)

    def getProjectID(self, zipname):
        projectID = ""
        p1 = self.getP1(zipname)
        match = self.parseProjectID(p1)
        if (match is not None):
            projectID = match.group(0)[0:-1]
        return projectID


    def getDeliveryID(self, zipname):
        deliveryID = ""
        pos = zipname.find('ARCSOFT_')
        if (pos > 0):
            head = zipname[0:pos-1]
            
            startPos = 0
            projectID = self.getProjectID(head)
            if (projectID is not None):
                startPos = len(projectID) + 1
            deliveryID = head[startPos:]
        return deliveryID


    def getProductName(self, zipname):
        p2 = self.getP2(zipname)

        endPos = -1
        match = self.parseVersion(p2)
        if (match is not None):
            endPos = match.start()
        
        startPos = 0
        match = re.search(r"ARCSOFT_", p2)
        if (match is not None):
            startPos = match.end()
        
        productName = p2[startPos:endPos]
        return productName

    def getVersion(self, zipname):
        version = ""
        match = self.parseVersion(zipname)
        if (match is not None):
            version = match.group(0)[1:-1]
        return version


    def getBuildDate(self, zipname):
        buildDate = ""
        match = self.parseBuildDate(zipname)
        if (match is not None):
            buildDate = match.group(0)[1:-1]
        return buildDate


    def parseBuildNumber(self, zipname):
        p5 = self.getP5(zipname)
        if (len(p5) == 0):
            return None
        # + : 1 or more
        # * : 0 or more
        pattern = r"\d+_{0,1}"
        return re.search(pattern, p5)

    def getBuildNumber(self, zipname):
        buildNumber = ""
        match = self.parseBuildNumber(zipname)
        if (match is not None):
            buildNumber = match.group(0)
            if (buildNumber[-1] == '_'):
                buildNumber = buildNumber[0:-1]
        return buildNumber

    def getPlatform(self, zipname):
        platform = ""
        p3 = self.getP3(zipname)
        remain = p3
        items = remain.split('_')
        # drop customer
        if (len(items) >= 2 and items[-2] == 'FOR'):
            remain = '_'.join(items[0:-2])
            items = remain.split('_')
        # drop eval
        if (items[-1] == 'EVAL'):
            remain = '_'.join(items[0:-1])
            items = remain.split('_')
        
        build_types = self.getSupportedBuildTypes()
        if (items[-1] in build_types):
            remain = '_'.join(items[0:-1])
        
        if (len(remain) != 0):
            platform = remain
        return platform

    def getPlatformTypeEvalCustomerStr(self, zipname):
        startPos = 0
        versionMatch = self.parseVersion(zipname)
        if (versionMatch is not None):
            startPos = versionMatch.end()

        endPos = -1
        buildDateMatch = self.parseBuildDate(zipname)
        if (buildDateMatch is not None):
            endPos = buildDateMatch.start()
        
        remain = zipname[startPos:endPos]
        return remain

    def getType(self, zipname):
        remain = self.getPlatformTypeEvalCustomerStr(zipname)
        items = remain.split('_')
        # drop customer
        if (len(items) >= 2 and items[-2] == 'FOR'):
            remain = '_'.join(items[0:-2])
            items = remain.split('_')
        # drop eval
        if (items[-1] == 'EVAL'):
            remain = '_'.join(items[0:-1])
            items = remain.split('_')
        type = items[-1]
        build_types = self.getSupportedBuildTypes()
        if (type not in build_types):
            type = ""
        return type

    def getEval(self, zipname):
        evalStr = ""
        remain = self.getPlatformTypeEvalCustomerStr(zipname)
        items = remain.split('_')
        # drop customer
        if (len(items) >= 2 and items[-2] == 'FOR'):
            remain = '_'.join(items[0:-2])
            items = remain.split('_')
        if (items[-1] == 'EVAL'):
            evalStr = "EVAL"
        return evalStr

    def getCustomer(self, zipname):
        customer = ""
        remain = self.getPlatformTypeEvalCustomerStr(zipname)
        items = remain.split('_')
        if (len(items) >= 2 and items[-2] == 'FOR'):
            customer = items[-1]
        return customer

    def getOther(self, zipname):
        other = ""
        p5 = self.getP5(zipname)
        if (len(p5) == 0):
            return other
        
        match = self.parseBuildNumber(zipname)
        startPos = match.end()

        p5 = self.getP5(zipname)
        remain = p5[startPos:]
        # print('startPos:', startPos)
        # print('in getOther: remain is {:s}'.format(remain))
        if (len(remain) != 0):
            other = remain
        return other

    def parse(self, zipname = None):
        if (zipname is not None):
            self.zipname = zipname
        pkg = DeliveryPackageName()
        pkg.projectID = self.getProjectID(self.zipname)
        pkg.deliveryID = self.getDeliveryID(self.zipname)
        pkg.productName = self.getProductName(self.zipname)
        pkg.version = self.getVersion(self.zipname)
        pkg.platform = self.getPlatform(self.zipname)
        pkg.type = self.getType(self.zipname)
        pkg.eval = self.getEval(self.zipname)
        pkg.customer = self.getCustomer(self.zipname)
        pkg.buildDate = self.getBuildDate(self.zipname)
        pkg.buildNumber = self.getBuildNumber(self.zipname)
        pkg.other = self.getOther(self.zipname)
        pkg.other = self.getOther(self.zipname)
        return pkg


class DeliveryPackageName(object):
    def __init__(self, zipname = ''):
        
        self.zipname = zipname

        self.projectID = ""
        self.deliveryID = ""
        self.productName = ""
        self.version = ""
        self.platform = ""
        self.type = ""
        self.eval = ""
        self.customer = ""
        self.buildDate = ""
        self.buildNumber = ""
        self.other = ""
    
    def isValid(self):
        if (not self.zipname.endswith('.zip')):
            print("Error: zipname not ends with .zip")
            return False
        if (self.productName == ""):
            print("Error: productName shouldn't be empty")
            return False
        if (self.version == ""):
            print("Error: version shouldn't be empty")
            return False
        if (self.buildDate == ""):
            print("Error: buildDate shouldn't be empty")
            return False
        if (self.buildNumber == ""):
            print("Error: buildNumber shouldn't be empty")
            return False
        return True
    
    def setProjectID(self, projectID):
        self.projectID = projectID
        return self

    def setDeliveryID(self, deliveryID):
        self.deliveryID = deliveryID
        return self
    
    def setProductName(self, productName):
        self.productName = productName
        return self
    
    def setVersion(self, version):
        self.version = version
        return self
    
    def setPlatform(self, platform):
        self.platform = platform
        return self
    
    def setType(self, type):
        self.type = type
        return self
    
    def setEval(self, eval):
        self.eval = eval
        return self
    
    def setCustomer(self, customer):
        self.customer = customer
        return self
    
    def setBuildDate(self, buildDate):
        self.buildDate = buildDate
        return self
    
    def setBuildNumber(self, buildNumber):
        self.buildNumber = buildNumber
        return self
    
    def setOther(self, other):
        self.other = other
        return self

    def makePrintItem(self, key, value):
        key = key + ":"
        return '{:s} {:s}'.format(key.ljust(13, ' '), value)

    def __str__(self):
        # for printing instance of DeliveryPackageName
        lines = []
        lines.append(self.makePrintItem('ProjectID', self.projectID))
        lines.append(self.makePrintItem('DeliveryID', self.deliveryID))
        lines.append(self.makePrintItem('ProductName', self.productName))
        lines.append(self.makePrintItem('Version', self.version))
        lines.append(self.makePrintItem('PLATFORM', self.platform))
        lines.append(self.makePrintItem('Type', self.type))
        lines.append(self.makePrintItem('Eval', self.eval))
        lines.append(self.makePrintItem('Customer', self.customer))
        lines.append(self.makePrintItem('BuildDate', self.buildDate))
        lines.append(self.makePrintItem('BuildNumer', self.buildNumber))
        lines.append(self.makePrintItem('Other', self.other))
        res = '\n'.join(lines)
        return res
    
    def getZipname(self):
        res = ""
        if (self.projectID != ""):
            res += "{:s}_".format(self.projectID)
        if (self.deliveryID != ""):
            res += "{:s}_".format(self.deliveryID)
        res += "ARCSOFT_{:s}_{:s}".format(self.productName, self.version)
        if (self.platform != ""):
            res += "_{:s}".format(self.platform)
        if (self.type != ""):
            res += "_{:s}".format(self.type)
        if (self.eval != ""):
            res += "_{:s}".format(self.eval)
        if (self.customer != ""):
            res += "_FOR_{:s}".format(self.customer)
        res += "_{:s}".format(self.buildDate)
        if (self.buildNumber != ""):
            if (self.buildDate.startswith("20")):
                res += "_{:s}".format(self.buildNumber)
            else:
                res += "_AUTOBUILD_{:s}".format(self.buildNumber)
        if (self.other != ""):
            res += "_{:s}".format(self.other)
        res += ".zip"
        return res






#--------------------------------------------------------------------------------
# Auto Unzipping
#--------------------------------------------------------------------------------

def unzip_file(zip_src, dst_dir):
    with zipfile.ZipFile(zip_src, mode="r") as archive:
        archive.extractall(path=dst_dir)

# 1. 解压多个文件
def unzip_package_zips(zippath_lst, temp_dir):
    """
    @param temp_dir: zip 解压的临时保存目录
    """
    for zippath in zippath_lst:
        print('unzipping ', zippath)
        unzip_file(zippath, temp_dir)

# 2. 扫描解压后的目录， 跳过 platform 目录， 只保留 windows 和 tda4 的目录
def get_candidate_dirs(temp_dir):
    """
    @return 列表， 每个元素是一个目录
    """
    candidate_dirs = []
    for item in os.listdir(temp_dir):
        if (item == "PLATFORM"):
            continue
        the_dir = os.path.join(temp_dir, item)
        if (the_dir):
            candidate_dirs.append(the_dir)
    return candidate_dirs


# 3. 扫描拷贝头文件
def copy_inc_dir(src_subdir, pkg_dir):
    """
    @param src_subdir 解压目录里 inc 的父目录。 例如 candidcate_dirs[0]
    @param pkg_dir 用来存放规整的 package 的目录
    """
    #print(subdir)
    src_inc_dir = src_subdir + "/inc"
    dst_inc_dir = pkg_dir + "/inc"
    # if (os.path.exists(dst_inc_dir)):
    #     shutil.rmtree(dst_inc_dir)
    shutil.copytree(src_inc_dir, dst_inc_dir, dirs_exist_ok=True)
    fpath = dst_inc_dir + "/adas_inner_public.h"
    if (os.path.exists(fpath)):
        os.remove(fpath)

# 4. 扫描拷贝 windows 库
def copy_lib_dir(candidate_dirs, pkg_dir, keyword_for_filter_dirs, save_platform_arch_lower):
    filtered_candidate_dirs = []
    for subdir in candidate_dirs:
        if keyword_for_filter_dirs in subdir:
            filtered_candidate_dirs.append(subdir)
    dst_lib_dir = pkg_dir + "/lib/" + save_platform_arch_lower
    if (os.path.exists(dst_lib_dir)):
        shutil.rmtree(dst_lib_dir)
    for subdir in filtered_candidate_dirs:
        src_lib_dir = subdir + "/lib/" + keyword_for_filter_dirs.lower()
        shutil.copytree(src_lib_dir, dst_lib_dir, dirs_exist_ok=True)

def copy_windows_x64_lib_dir(candidate_dirs, pkg_dir, vs_platform_arch_upper, keyword=None):
    if keyword is None:
        keyword = vs_platform_arch_upper
    copy_lib_dir(candidate_dirs, pkg_dir, keyword, vs_platform_arch_upper.lower())

# 4. 扫描拷贝 tda4 库
def copy_tda4_lib_dir(candidate_dirs, pkg_dir, platform_arch_upper="LINUX_ARM64_TDA4", keyword=None):
    if keyword is None:
        keyword = platform_arch_upper
    copy_lib_dir(candidate_dirs, pkg_dir, keyword, platform_arch_upper.lower())

# 5. 写 cmakelist
def determine_lib_mode(window_x64_lib_names):
    """
    @brief 根据给定的几个库名称， 判断是否包含 debug 库
    @return 1: 是release库
            2: 有debug库
    NOTE: 假定了要么是一个库文件， 要么是两个库 并且一个是releae的 另一个是debug的
    """
    lib_mode = 1 # single lib
    # print(window_x64_lib_names[0])
    # print(window_x64_lib_names[1])
    #print('len(window_x64_lib_names)', len(window_x64_lib_names))

    lib_names = []
    dll_names = []
    for item in window_x64_lib_names:
        print(item)
        if (item.endswith('.lib')):
            lib_names.append(item)
        elif (item.endswith('.dll')):
            dll_names.append(item)

    print('lib_names:')
    for name in lib_names:
        print(name)
    if (len(dll_names) > 0):
        print('dll_names:')
        for name in dll_names:
            print(name)

    if (len(lib_names) == 2):
        if (len(lib_names[0]) > len(lib_names[1])):
            lib_names[1], lib_names[0] = lib_names[0], lib_names[1]
            if (len(dll_names) == 2):
                dll_names[1], dll_names[0] = dll_names[0], dll_names[1]
        len1 = len(lib_names[0])
        len2 = len(lib_names[1])
        # print('len1 = ', len1)
        # print('len2 = ', len2)
        if ((len1 + 1 == len2) or (len1 + 2 == len2)) and (lib_names[1][-5] == 'd'):
            lib_mode = 2
    #print('len(window_x64_lib_names)', len(names))
    return lib_mode, lib_names, dll_names


def get_vs_platform_arch_and_version(zippath_lst):
    platform_archs = set()
    pkg_windows_versions = []
    for zippath in zippath_lst:
        zipname = os.path.split(zippath)[-1]
        pkg = DeliveryPackageNameParser(zipname).parse()
        if (pkg.platform in ['VS2015_X64', 'VS2017_X64', 'VS2019_X64', 'VS2022_X64']):
            platform_archs.add(pkg.platform.lower())
            pkg_windows_versions.append(pkg.version)
    if (len(platform_archs) != 1):
        print('Error! 0 or more than one platform arch found')
        exit(1)
    vs_platform_arch = list(platform_archs)[0]

    versions = list(set(pkg_windows_versions))
    if (len(versions) != 1):
        print("Error! 0 or more than one version found")
    windows_pkg_version = versions[0]

    return vs_platform_arch, windows_pkg_version


def get_tda4_pkg_version(zippath_lst):
    tda4_pkg_version = None
    for zippath in zippath_lst:
        zipname = os.path.split(zippath)[-1]
        pkg = DeliveryPackageNameParser(zipname).parse()
        if (pkg.platform == 'LINUX_ARM64_TDA4_A'):
            tda4_pkg_version = pkg.version
            break
    return tda4_pkg_version


def get_versions(zippath_lst):
    versions = []
    for zippath in zippath_lst:
        zipname = os.path.split(zippath)[-1]
        pkg = DeliveryPackageNameParser(zipname).parse()
        versions.append(pkg.version)
    return list(set(versions))


def generate_cmake_lib_path_location(platform_arch, libname):
    return "${CMAKE_CURRENT_SOURCE_DIR}" + "/lib/" + platform_arch + "/" + libname

def write_cmakelist(pkg_dir, pkg_name, require_lst, vs_platform_arch, windows_pkg_version=None, tda4_pkg_version=None):
    # vs2017x64
    windows_x64_lib_dir = pkg_dir + "/lib/" + vs_platform_arch
    windows_x64_lib_names = []
    for item in os.listdir(windows_x64_lib_dir):
        windows_x64_lib_names.append(item)

    lib_mode, lib_names, dll_names = determine_lib_mode(windows_x64_lib_names)
    lib_prop_lines = []
    print('lib_mode:', lib_mode)

    tda4_target_type = 'STATIC'
    if (len(dll_names) == 0):
        windows_target_type = 'STATIC'
    else:
        windows_target_type = 'SHARED'
    if (lib_mode == 1):
        lib_location = generate_cmake_lib_path_location(vs_platform_arch, lib_names[0])

        if (len(dll_names) == 0):
            lib_prop_lines.append('        IMPORTED_LOCATION "{:s}"'.format(lib_location))
        else:
            dll_location = generate_cmake_lib_path_location(vs_platform_arch, dll_names[0])
            lib_prop_lines.append('        IMPORTED_LOCATION "{:s}"'.format(dll_location))
            lib_prop_lines.append('        IMPORTED_IMPLIB "{:s}"'.format(lib_location))
    elif (lib_mode == 2):
        windows_x64_debug_lib_path = lib_names[1]
        windows_x64_release_lib_path = lib_names[0]
        debug_lib_location = generate_cmake_lib_path_location(vs_platform_arch, windows_x64_debug_lib_path)
        release_lib_location = generate_cmake_lib_path_location(vs_platform_arch, windows_x64_release_lib_path)
        
        if (len(dll_names) == 0):
            lib_prop_lines.append('        IMPORTED_LOCATION_DEBUG "{:s}"'.format(debug_lib_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_RELEASE "{:s}"'.format(release_lib_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_MINSIZEREL "{:s}"'.format(release_lib_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_RELWITHDEBINFO "{:s}"'.format(release_lib_location))
        else:
            debug_dll_name = dll_names[1]
            release_dll_name = dll_names[0]
            debug_dll_location = generate_cmake_lib_path_location(vs_platform_arch, debug_dll_name)
            release_dll_location = generate_cmake_lib_path_location(vs_platform_arch, release_dll_name)
            
            lib_prop_lines.append('        IMPORTED_LOCATION_DEBUG "{:s}"'.format(debug_dll_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_RELEASE "{:s}"'.format(release_dll_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_MINSIZEREL "{:s}"'.format(release_dll_location))
            lib_prop_lines.append('        IMPORTED_LOCATION_RELWITHDEBINFO "{:s}"'.format(release_dll_location))

            lib_prop_lines.append('        IMPORTED_IMPLIB_DEBUG "{:s}"'.format(debug_lib_location))
            lib_prop_lines.append('        IMPORTED_IMPLIB_RELEASE "{:s}"'.format(release_lib_location))
            lib_prop_lines.append('        IMPORTED_IMPLIB_MINSIZEREL "{:s}"'.format(release_lib_location))
            lib_prop_lines.append('        IMPORTED_IMPLIB_RELWITHDEBINFO "{:s}"'.format(release_lib_location))

    # tda4
    tda4_lib_dir_midfix = "lib/linux_arm64_tda4"
    tda4_lib_dir = pkg_dir + "/" + tda4_lib_dir_midfix
    tda4_lib_name = os.listdir(tda4_lib_dir)[0]
    print('tda4_lib_name:', tda4_lib_name)
    tda4_lib_location = "${CMAKE_CURRENT_SOURCE_DIR}" + "/lib/linux_arm64_tda4/{:s}".format(tda4_lib_name)
    #tda4_lib_location = generate_cmake_lib_path_location(tda4_lib_dir_midfix, tda4_lib_name)

    cmake_lines = []
    cmake_lines.append("")
    cmake_lines.append('if(CMAKE_SYSTEM_NAME MATCHES "Windows")')
    cmake_lines.append("    add_library({:s} {:s} IMPORTED GLOBAL)".format(pkg_name, windows_target_type))
    cmake_lines.append('    set_target_properties({:s} PROPERTIES'.format(pkg_name))
    cmake_lines.append('        INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/inc"')
    for line in lib_prop_lines:
        cmake_lines.append(line)
        # cmake_lines.append('        IMPORTED_LOCATION_DEBUG "{:s}"'.format(windows_x64_debug_lib_path))
        # cmake_lines.append('        IMPORTED_LOCATION_RELEASE "{:s}"'.format(windows_x64_release_lib_path))
        # cmake_lines.append('        IMPORTED_LOCATION_MINSIZEREL "{:s}"'.format(windows_x64_release_lib_path))
        # cmake_lines.append('        IMPORTED_LOCATION_RELWITHDEBINFO "{:s}"'.format(windows_x64_release_lib_path))
    if (windows_pkg_version is not None):
        cmake_lines.append("        VERSION {:s}".format(windows_pkg_version))
    cmake_lines.append('    )')
    cmake_lines.append('else() # tda4')
    cmake_lines.append("    add_library({:s} {:s} IMPORTED GLOBAL)".format(pkg_name, tda4_target_type))
    cmake_lines.append('    set_target_properties({:s} PROPERTIES'.format(pkg_name))
    cmake_lines.append('        INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/inc"')
    cmake_lines.append('        IMPORTED_LOCATION "{:s}"'.format(tda4_lib_location))
    if (tda4_pkg_version is not None):
        cmake_lines.append("        VERSION {:s}".format(tda4_pkg_version))
    cmake_lines.append('    )')
    cmake_lines.append('endif()')



    if (len(require_lst) != 0):
        cmake_lines.append("")
        cmake_lines.append('target_link_libraries({:s} INTERFACE'.format(pkg_name))
        for item in require_lst:
            cmake_lines.append('    {:s}'.format(item))
        cmake_lines.append(')')

    cmakelists_txt_path = '{:s}/CMakeLists.txt'.format(pkg_dir)
    fout = open(cmakelists_txt_path, "w")
    for line in cmake_lines:
        fout.write(line + "\n")
    fout.close()


class AutoUnzipper(object):
    def __init__(self, zippath_lst, temp_dir, pkg_dir, pkg_name, require_lst):
        self.zippath_lst = zippath_lst
        self.temp_dir = temp_dir
        self.pkg_dir = pkg_dir
        self.pkg_name = pkg_name
        self.require_lst = require_lst

        # validate zippath_lst
        for zippath in self.zippath_lst:
            if (not zippath.endswith('.zip')):
                print("Error: filename not endswith .zip:", zippath)
                exit(1)
    
    def run(self, tda4_keyword=None):
        vs_platform_arch, windows_pkg_version = get_vs_platform_arch_and_version(self.zippath_lst)
        tda4_pkg_version = get_tda4_pkg_version(self.zippath_lst)
        print('tda4_pkg_version:', tda4_pkg_version)
        unzip_package_zips(self.zippath_lst, self.temp_dir)
        candidate_dirs = get_candidate_dirs(self.temp_dir)
        copy_inc_dir(candidate_dirs[0], self.pkg_dir)
        copy_windows_x64_lib_dir(candidate_dirs, self.pkg_dir, vs_platform_arch.upper())
        copy_tda4_lib_dir(candidate_dirs, self.pkg_dir, keyword=tda4_keyword)
        write_cmakelist(self.pkg_dir, self.pkg_name, self.require_lst, vs_platform_arch, windows_pkg_version=windows_pkg_version, tda4_pkg_version=tda4_pkg_version)



def copy_toycv_lib_dir(temp_dir, pkg_dir, save_dir_midfix):
    src_lib_dir = temp_dir + "/lib"
    dst_lib_dir = pkg_dir + "/" + save_dir_midfix
    if (os.path.exists(dst_lib_dir)):
        shutil.rmtree(dst_lib_dir)
    shutil.copytree(src_lib_dir, dst_lib_dir)

def parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst):
    """
    zippaths = [
        "toy_core-1.3.2-vs2015-x64-static.zip",
        "toy_core-1.3.2-linux-aarch64-static.zip"
    ]
    temp_dir = "temp_toy_core"
    pkg_dir = "toy_core"
    pkg_name = "toy_core"
    """
    version = os.path.split(zippaths[0])[-1].split('-')[1]
    vs_platform_arch = 'vs2015_x64'
    for zippath in zippaths:
        if ('vs2015-x64' in zippath):
            midfix = 'lib/vs2015_x64'
            sub_temp_dir = temp_dir + "/windows"
        elif ('linux-aarch64' in zippath):
            midfix = 'lib/linux_arm64_tda4'
            sub_temp_dir = temp_dir + "/tda4"
        
        only_one_zippaths = [zippath]
        unzip_package_zips(only_one_zippaths, sub_temp_dir)
        copy_inc_dir(sub_temp_dir, pkg_dir)
        copy_toycv_lib_dir(sub_temp_dir, pkg_dir, midfix)
    write_cmakelist(pkg_dir, pkg_name, require_lst, vs_platform_arch, windows_pkg_version=version, tda4_pkg_version=version)


def parse_toy_core(toycv_version, prefix):
    zippaths = [
        prefix + "toy_core-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_core-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_core"
    pkg_dir = "toy_core"
    pkg_name = "toy_core"
    require_lst = []

    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)

def parse_toy_imgproc(toycv_version, prefix):
    zippaths = [
        prefix + "toy_imgproc-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_imgproc-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_imgproc"
    pkg_dir = "toy_imgproc"
    pkg_name = "toy_imgproc"
    require_lst = ["toy_core"]
    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)

def parse_toy_fourcc(toycv_version, prefix):
    zippaths = [
        prefix + "toy_fourcc-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_fourcc-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_fourcc"
    pkg_dir = "toy_fourcc"
    pkg_name = "toy_fourcc"
    require_lst = ["toy_imgproc", "toy_core"]
    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)

def parse_toy_shape_analysis(toycv_version, prefix):
    zippaths = [
        prefix + "toy_shape_analysis-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_shape_analysis-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_shape_analysis"
    pkg_dir = "toy_shape_analysis"
    pkg_name = "toy_shape_analysis"
    require_lst = ["toy_imgproc", "toy_core"]
    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)

def parse_toy_calib3d(toycv_version, prefix):
    zippaths = [
        prefix + "toy_calib3d-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_calib3d-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_calib3d"
    pkg_dir = "toy_calib3d"
    pkg_name = "toy_calib3d"
    require_lst = ["toy_imgproc", "toy_core"]
    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)

def parse_toy_imageio(toycv_version, prefix):
    zippaths = [
        prefix + "toy_imageio-{:s}-linux-aarch64-static.zip".format(toycv_version),
        prefix + "toy_imageio-{:s}-vs2015-x64-static.zip".format(toycv_version),
    ]
    temp_dir = "temp/toy_imageio"
    pkg_dir = "toy_imageio"
    pkg_name = "toy_imageio"
    require_lst = ["toy_imgproc", "toy_core"]
    parse_toycv_module(zippaths, temp_dir, pkg_dir, pkg_name, require_lst)





class ParseDeliveryPackageNameTest(unittest.TestCase):
    def assertResultEqual(self, expected, actual):
        # print('actual:')
        # print(actual)
        # print('expected:')
        # print(expected)
        
        if (expected.projectID != actual.projectID):
            self.fail('projectID did not match: expected: {!r}, actual: {!r}'.format(expected.projectID, actual.projectID))

        if (expected.deliveryID != actual.deliveryID):
            self.fail('deliveryID did not match: expected: {!r}, actual: {!r}'.format(expected.deliveryID, actual.deliveryID))

        if (expected.productName != actual.productName):
            self.fail('productName did not match: expected: {!r}, actual: {!r}'.format(expected.productName, actual.productName))

        if (expected.version != actual.version):
            self.fail('version did not match: expected: {!r}, actual: {!r}'.format(expected.version, actual.version))

        if (expected.platform != actual.platform):
            self.fail('platform did not match: expected: {!r}, actual: {!r}'.format(expected.platform, actual.platform))

        if (expected.type != actual.type):
            self.fail('type did not match: expected: {!r}, actual: {!r}'.format(expected.type, actual.type))

        if (expected.eval != actual.eval):
            self.fail('eval did not match: expected: {!r}, actual: {!r}'.format(expected.eval, actual.eval))

        if (expected.customer != actual.customer):
            self.fail('customer did not match: expected: {!r}, actual: {!r}'.format(expected.customer, actual.customer))

        if (expected.buildDate != actual.buildDate):
            self.fail('buildDate did not match: expected: {!r}, actual: {!r}'.format(expected.buildDate, actual.buildDate))

        if (expected.buildNumber != actual.buildNumber):
            self.fail('buildNumber did not match: expected: {!r}, actual: {!r}'.format(expected.buildNumber, actual.buildNumber))

        if (expected.other != actual.other):
            self.fail('other did not match: expected: {!r}, actual: {!r}'.format(expected.other, actual.other))

    def test_case1(self):
        zipname = "10836_D1_ARCSOFT_BODYTRACKING_1.0.120211001.5_STATIC_EVAL_FOR_SAMSUNG_20160613_1731_LOG.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("10836")
        expected.setDeliveryID("D1")
        expected.setProductName("BODYTRACKING")
        expected.setVersion("1.0.120211001.5")
        expected.setPlatform("")
        expected.setType("STATIC")
        expected.setEval("EVAL")
        expected.setCustomer("SAMSUNG")
        expected.setBuildDate("20160613")
        expected.setBuildNumber("1731")
        expected.setOther("LOG")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case2(self):
        zipname = "10836_D1_ARCSOFT_BODYTRACKING_1.0.120211001.5_Android_arm32_STATIC_EVAL_FOR_SAMSUNG_20160613_1731_Revision3942.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("10836")
        expected.setDeliveryID("D1")
        expected.setProductName("BODYTRACKING")
        expected.setVersion("1.0.120211001.5")
        expected.setPlatform("Android_arm32")
        expected.setType("STATIC")
        expected.setEval("EVAL")
        expected.setCustomer("SAMSUNG")
        expected.setBuildDate("20160613")
        expected.setBuildNumber("1731")
        expected.setOther("Revision3942")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case3(self):
        zipname = "10836_D1_ARCSOFT_BODYTRACKING_1.0.120211001.5_JAVASDK_EVAL_FOR_SAMSUNG_20160613_1731_Revision3942.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("10836")
        expected.setDeliveryID("D1")
        expected.setProductName("BODYTRACKING")
        expected.setVersion("1.0.120211001.5")
        expected.setPlatform("JAVASDK")
        expected.setType("")
        expected.setEval("EVAL")
        expected.setCustomer("SAMSUNG")
        expected.setBuildDate("20160613")
        expected.setBuildNumber("1731")
        expected.setOther("Revision3942")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case4(self):
        zipname = "ARCSOFT_BODYTRACKING_1.0.12021.5_20160613_1731.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("BODYTRACKING")
        expected.setVersion("1.0.12021.5")
        expected.setPlatform("")
        expected.setType("")
        expected.setEval("")
        expected.setCustomer("")
        expected.setBuildDate("20160613")
        expected.setBuildNumber("1731")
        expected.setOther("")
        
        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case5(self):
        zipname = "ARCSOFT_ADAS_ASCC_2.0.21623.1_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_34.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_ASCC")
        expected.setVersion("2.0.21623.1")
        expected.setPlatform("LINUX_ARM64_TDA4_A")
        expected.setType("")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("03222023")
        expected.setBuildNumber("34")
        expected.setOther("")
        
        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case6(self):
        zipname = "ARCSOFT_ADAS_ASCC_2.0.30102.1_VS2015_X64_STATIC_FOR_ARCSOFT_03222023_AUTOBUILD_56_DEBUG.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_ASCC")
        expected.setVersion("2.0.30102.1")
        expected.setPlatform("VS2015_X64")
        expected.setType("STATIC")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("03222023")
        expected.setBuildNumber("56")
        expected.setOther("DEBUG")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case7(self):
        zipname = "ARCSOFT_ADAS_ENCODE_1.3.21623.23005_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_03222023_AUTOBUILD_13.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_ENCODE")
        expected.setVersion("1.3.21623.23005")
        expected.setPlatform("LINUX_ARM64_TDA4_A")
        expected.setType("")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("03222023")
        expected.setBuildNumber("13")
        expected.setOther("")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case8(self):
        zipname = "ARCSOFT_ADAS_IR_NIGHT_CONTOUR_2.0.0.2_TDA4_FOR_ARCSOFT_03302023.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_IR_NIGHT_CONTOUR")
        expected.setVersion("2.0.0.2")
        expected.setPlatform("TDA4")
        expected.setType("")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("03302023")
        expected.setBuildNumber("")
        expected.setOther("")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case9(self):
        zipname = "ARCSOFT_IR_NIGHT_CONTOUR_2.0.21623.3_LINUX_ARM64_TDA4_A_FOR_ARCSOFT_04012023_AUTOBUILD_3.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("IR_NIGHT_CONTOUR")
        expected.setVersion("2.0.21623.3")
        expected.setPlatform("LINUX_ARM64_TDA4_A")
        expected.setType("")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("04012023")
        expected.setBuildNumber("3")
        expected.setOther("")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case10(self):
        zipname = "ARCSOFT_UNDISTORT_POINTS_0.0.30302.6_VS2017_X64_SHARED_FOR_ARCSOFT_04062023_AUTOBUILD_20_DEBUG.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("UNDISTORT_POINTS")
        expected.setVersion("0.0.30302.6")
        expected.setPlatform("VS2017_X64")
        expected.setType("SHARED")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("04062023")
        expected.setBuildNumber("20")
        expected.setOther("DEBUG")
        
        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())


    def test_case11(self):
        zipname = "ARCSOFT_ADAS_LD_2.9.30302.3_VS2017_X64_STATIC_FOR_ARCSOFT_04072023_AUTOBUILD_62.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_LD")
        expected.setVersion("2.9.30302.3")
        expected.setPlatform("VS2017_X64")
        expected.setType("STATIC")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("04072023")
        expected.setBuildNumber("62")
        expected.setOther("")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())

    def test_case12(self):
        zipname = "ARCSOFT_ADAS_CALIBINNER_1.0.30302.21_VS2017_X64_STATIC_FOR_ARCSOFT_04102023_AUTOBUILD_23.zip"
        actual = DeliveryPackageNameParser().parse(zipname)

        expected = DeliveryPackageName()
        expected.setProjectID("")
        expected.setDeliveryID("")
        expected.setProductName("ADAS_CALIBINNER")
        expected.setVersion("1.0.30302.21")
        expected.setPlatform("VS2017_X64")
        expected.setType("STATIC")
        expected.setEval("")
        expected.setCustomer("ARCSOFT")
        expected.setBuildDate("04102023")
        expected.setBuildNumber("23")
        expected.setOther("")

        self.assertResultEqual(expected, actual)
        self.assertEqual(zipname, actual.getZipname())

def parse_package_example():
    zipname = "10836_D1_ARCSOFT_BODYTRACKING_1.0.120211001.5_STATIC_EVAL_FOR_SAMSUNG_20160613_1731_LOG.zip"
    parser = DeliveryPackageNameParser(zipname)
    print("P1:", parser.getP1(zipname))
    print("P2:", parser.getP2(zipname))
    print("P3:", parser.getP3(zipname))
    print("P4:", parser.getP4(zipname))
    print("P5:", parser.getP5(zipname))
    
    pkg = parser.parse()
    print("pkg:")
    print(pkg)

def make_package_example():
    pkg = DeliveryPackageName()
    pkg.setProjectID("10836")
    pkg.setDeliveryID("D1")
    pkg.setProductName("BODYTRACKING")
    pkg.setVersion("1.0.120211001.5")
    pkg.setPlatform("")
    pkg.setType("STATIC")
    pkg.setEval("EVAL")
    pkg.setCustomer("SAMSUNG")
    pkg.setBuildDate("20160613")
    pkg.setBuildNumber("1731")
    pkg.setOther("LOG")

    print("pkg.zipname:", pkg.getZipname())

#--------------------------------------------------------------------------------
# remake `strings` command in Python
#--------------------------------------------------------------------------------
def strings(fname):
    from mmap import mmap, ACCESS_READ
    import re
    """
    This function behaves like `strings` command in linux/windows.
    If no desired result returned, you may just tweak the regular expression pattern.
    ref: https://gist.github.com/berdario/114b2daf9b43fe924676
    """
    pattern = '([\w/.\s(:)-]{10,60})'
    with open(fname, 'rb') as f, mmap(f.fileno(), 0, access=ACCESS_READ) as m:
        for match in re.finditer(pattern.encode(), m):
            yield match.group(0)

if __name__ == '__main__':
    unittest.main(testRunner=MyTestRunner())

    # parse_package_example()
    # make_package_example()