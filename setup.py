#!/usr/bin/env python
from setuptools import setup

__version__ = ""
exec(open("src/duplicates/_version.py").read())

with open("requirements.txt") as f:
    required = [l for l in f.read().splitlines() if not l.startswith("#")]

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="duplicates",
    version=__version__,
    description="Browse a directory tree and search for duplicate files and directories",
    long_description=long_description,
    keywords="git, client, terminal, console",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Recovery Tools",
        "Topic :: Utilities",
        ],
    author="Tim Legrand",
    author_email="timlegrand.perso+dev@gmail.com",
    url="https://github.com/timlegrand/duplicates",
    download_url="https://github.com/timlegrand/duplicates",
    license="BSD 2-Clause",
    packages=["duplicates"],
    package_dir={"": "src"},
    install_requires=required,
    entry_points={"console_scripts": ["duplicates = duplicates.duplicates:_main"]},
    )
