"""
Author:     David Walshe
Date:       08 April 2021
"""

import os
import json
from setuptools import setup
from setuptools import find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read_readme() -> str:
    """
    Returns the content of the README.md.
    """
    return open(os.path.join(os.path.dirname(__file__), "README.md")).read()


def __version__() -> str:
    """Returns the current tool version"""
    version_file_path = os.path.join(os.path.dirname(__file__), ".versioning.json")

    with open(version_file_path) as fh:
        content = json.load(fh)

    return content["version"]


setup(
    name="sla-cli",  # Replace with your own username
    version=__version__(),
    author="David Walshe",
    author_email="david.walshe93@gmail.com",
    description="A CLI tool designed to help source data for skin lesion research.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DavidWalshe93/SL-CLI",
    project_urls={
        "Homepage": "https://github.com/DavidWalshe93/SL-CLI",
        "Bug Tracker": "https://github.com/DavidWalshe93/SL-CLI/issues",
    },
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'Natural Language :: English',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        "Operating System :: OS Independent",
    ],
    keywords="cancer-research cancer skin-lesion skin lesion melanoma datasets data "
             "data-acquisition research skin-cancer utility tool academic download "
             "downloader isic MEDNODE DermIS DermQuest PAD-UFES-20 MClass "
             "Atlas-of-Dermascopy HAM10000 BCN20000 DERMOFIT cli command-line-tool".split(),

    # Python centric setup.
    packages=find_packages(),
    package_dir={"sla_cli": "."},
    python_requires=">=3.6",
    py_modules=["cli"],
    data_files=[("", ['LICENSE'])],
    include_package_data=True,
    install_requires=[
        "Click",
        "PyYAML",
        "Pandas",
        "tabulate",
        "attrs"
    ],
    entry_points='''
        [console_scripts]
        sla-cli=src.sla_cli:cli
    '''
)
