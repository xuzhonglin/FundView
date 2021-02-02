#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/29 11:05
@Author   : colinxu
@File     : build.py
@Desc     : 构建应用包
"""
import sys
import os
import subprocess

BUILD_PACKNAME = '韭菜盒子'
BUILD_VERSION = '1.2.4'


def build_win32():
    with open('venv/Scripts/activate.bat', 'r') as f:
        source_script = f.read()
    bat_content = '@echo off\n'
    bat_content += 'cd ' + os.getcwd() + '\n'
    bat_content += source_script + '\n'
    bat_content += 'cd ' + os.getcwd() + '\n'
    bat_content += 'chcp 65001 \n'
    bat_content += '@echo on\n'
    bat_content += 'pyinstaller -F -w --icon="form\\icon_windows.ico" -n {}-{} main.py\n'.format(BUILD_PACKNAME,
                                                                                                 BUILD_VERSION)
    bat_content += 'del {}-{}.spec\n'.format(BUILD_PACKNAME, BUILD_VERSION)
    with open('build.bat', 'w', encoding=sys.getdefaultencoding()) as f:
        f.write(bat_content)
    p = subprocess.Popen("build.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.readline()
    while out != b'':
        temp = bytes.decode(out).replace('\r\n', '')
        print(temp)
        out = p.stdout.readline()
    p.wait()

    if p.returncode == 0:
        os.remove('build.bat')
        print('build package success!!!')
    else:
        print('build package failed!!!')


def build_darwin():
    pass


if __name__ == '__main__':
    if sys.platform == 'darwin':
        build_darwin()
    else:
        build_win32()
