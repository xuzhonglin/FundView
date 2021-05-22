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

BUILD_PACKNAME = 'LeekBox'
BUILD_VERSION = '1.3.0'


def build_win32():
    with open('venv/Scripts/activate.bat', 'r') as f:
        source_script = f.read()
    cmd_content = '@echo off\n'
    cmd_content += 'cd ' + os.getcwd() + '\n'
    cmd_content += source_script + '\n'
    cmd_content += 'cd ' + os.getcwd() + '\n'
    cmd_content += 'chcp 65001 \n'
    cmd_content += '@echo on\n'
    cmd_content += 'pyinstaller -F -w --icon="form\\leekbox-icon-256.ico" -n {}-{} main.py\n'.format(BUILD_PACKNAME,
                                                                                                     BUILD_VERSION)
    cmd_content += 'del {}-{}.spec\n'.format(BUILD_PACKNAME, BUILD_VERSION)
    with open('build.bat', 'w', encoding=sys.getdefaultencoding()) as f:
        f.write(cmd_content)
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
    with open('venv/bin/activate', 'r') as f:
        source_script = f.read()
    cmd_content = source_script + '\n'
    cmd_content += 'cd ' + os.getcwd() + '\n'
    cmd_content += 'pyinstaller -F -w -y --icon="form/leekbox-icon-256.ico" -n {}-{} main.py\n'.format(BUILD_PACKNAME,
                                                                                                    BUILD_VERSION)

    cmd_content += 'rm {}-{}.spec\n'.format(BUILD_PACKNAME, BUILD_VERSION)
    with open(os.getcwd() + '/build.sh', 'w', encoding=sys.getdefaultencoding()) as f:
        f.write(cmd_content)
    subprocess.call('chmod a+x ' + os.getcwd() + '/build.sh', shell=True)
    p = subprocess.Popen(os.getcwd() + '/build.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.readline()
    while out != b'':
        temp = bytes.decode(out).replace('\n', '')
        print(temp)
        out = p.stdout.readline()
    p.wait()
    if p.returncode == 0:
        os.remove('build.sh')
        print('build package success!!!')
    else:
        print('build package failed!!!')


if __name__ == '__main__':
    if sys.platform == 'win32':
        build_win32()
    else:
        build_darwin()
