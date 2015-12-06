from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sdl2hl',
    version='0.2.1',

    description='A Pythonic API wrapper for SDL2.',
    long_description=long_description,

    url='https://github.com/jdoda/sdl2hl',
    author='Jonathan Doda',
    author_email='jonathan@jdoda.ca',

    license='zlib',
    keywords=['sdl2', 'cffi'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: zlib/libpng License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=['sdl2hl'],
    test_suite='tests',

    install_requires=[
        'enum34>=1.0.0',
        'sdl2-cffi>=1.0.0',
    ],
)
