#! /usr/bin/env python
#################################################################################
#     File Name           :     lsol/setup.py.in
#     Created By          :     yuewu
#     Description         :
#################################################################################

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from Cython.Build import cythonize

import sys
import os

sys.path.append("python/lsol")


def get_source_files(root_dir):
    src_files = []
    for pathname in os.listdir(root_dir):
        path = os.path.join(root_dir, pathname)
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext in ['.cc', '.cpp', '.c']:
                src_files.append(path)
        elif os.path.isdir(path):
            src_files = src_files + get_source_files(path)
    return src_files
def get_include_dirs():
    import numpy as np
    return [np.get_include(), "include", "external"]

if os.name == 'nt':
    extra_flags = ['/wd4251','/wd4275', '/EHsc','-DLSOL_EMBED_PACKAGE']
    dependencies = []
else:
    extra_flags = ['-std=c++11']
    dependencies = [
        "numpy      >= 1.7.0",
        "cython     >= 0.23.0",
        "scipy      >= 0.13.0",
        "setuptools"
        ]


ext_modules = [
    Extension(
        "pylsol",
        sources=["python/lsol/pylsol.pyx"] + get_source_files('src/lsol') +
        get_source_files('external/json'),
        language='c++',
        include_dirs=get_include_dirs(),
        extra_compile_args=['-DHAS_NUMPY_DEV', '-DUSE_STD_THREAD'] + extra_flags)
]


setup(
    name='lsol',
    version='1.1.0',
    description='Library for Scalable Online Learning',
    author='Yue Wu, Chenghao Liu, Steven C.H. Hoi',
    author_email='yuewu@outlook.com',
    maintainer='Yue Wu, Chenghao Liu',
    maintainer_email='yuewu@outlook.com',
    url='http://libsol.stevenhoi.org',
    license='Apache 2.0',
    packages=['', 'lsol'],
    package_dir={'': 'python'},
    entry_points = {
        'console_scripts':[
            'libsol_train=lsol.libsol_train:main',
            'libsol_test=lsol.libsol_test:main',
            ],
        },
    ext_modules=cythonize(ext_modules),
    install_requires=dependencies
    )