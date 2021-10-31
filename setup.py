# Copyright (c) 2021, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

from setuptools import setup, find_packages
import subprocess


def get_latest_tag():
    try:
        cmd_output = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"], stdout=subprocess.PIPE
        )
        return cmd_output.stdout.strip().decode("utf-8")
    except EnvironmentError:
        print("Couldn't run git to get a version number for setup.py")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ctorrent",
    version=get_latest_tag(),
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Curses Torrent Browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/ctorrent",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    install_requires=["requests", "ctable"],
    entry_points={
        "console_scripts": [
            "ctorrent = ctorrent.__main__:main",
        ],
    },
)
