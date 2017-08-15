# -*- coding: utf-8 -*-

from distutils.core import setup

from npgameworld import __version__

setup(
    name='npgameworld',
    version=__version__,
    license='zlib/libpng',
    url='https://github.com/xxblx/npgameworld',

    author='Oleg Kozlov',
    author_email='xxblx@posteo.org',

    description='Simple pure python game engine',
    long_description="""NpGameWorld is very simple pure python game engine
created for embedding. It designed for games like top-down shooters where
player controlls Hero by sending commands to world.""",

    platforms=['any'],

    packages=['npgameworld'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: zlib/libpng License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment'
    ],
    keywords='games game world engine shooter'
)
