"""
Author:     David Walshe
Date:       08 April 2021
"""

import os
import re
import codecs

from setuptools import setup
from setuptools import find_packages

PROJECT_URLS = {
    "Homepage": "https://github.com/DavidWalshe93/SL-CLI",
    "Bug Tracker": "https://github.com/DavidWalshe93/SL-CLI/issues",
}

CLASSIFIERS = [
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',

    "Operating System :: OS Independent",
]

KEYWORDS = "cancer-research cancer skin-lesion skin lesion melanoma datasets data " \
           "data-acquisition research skin-cancer utility tool academic download " \
           "downloader isic MEDNODE DermIS DermQuest PAD-UFES-20 MClass " \
           "Atlas-of-Dermascopy HAM10000 BCN20000 DERMOFIT cli command-line-tool".split()

INSTALL_REQUIRES = [
    "attrs",
    "click",
    "colorama",
    "coverage",
    "matplotlib",
    "numpy",
    "packaging",
    "pandas",
    "PyYAML",
    "tabulate"
]

CWD = os.path.abspath(os.path.dirname(__file__))


def get_metadata(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(CWD, *parts), "rb", "utf-8") as f:
        return f.read()


META_PATH = os.path.join(CWD, "sla_cli", "__init__.py")
META_FILE = get_metadata(META_PATH)


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    meta_match = re.search(
        rf"^__{meta}__ = ['\"]([^'\"]*)['\"]", META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


def read_readme() -> str:
    """Returns the content of the README.md."""
    with open(os.path.join(CWD, "README.md")) as fh:
        return fh.read()


if __name__ == '__main__':
    setup(
        name="sla-cli",
        version=find_meta("version"),
        author="David Walshe",
        author_email="david.walshe93@gmail.com",
        description="A CLI tool designed to help source data for skin lesion research.",
        long_description=read_readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/DavidWalshe93/SL-CLI",
        project_urls=PROJECT_URLS,
        license='MIT',
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,

        packages=find_packages(exclude=("tests", ".hooks")),
        python_requires=">=3.6",
        data_files=[
            ("", ['LICENSE']),
            ("sla_cli/db", ["sla_cli/db/db.json"]),
            ("sla_cli/src/common/logger", ["sla_cli/src/common/logger/logger_config.yml"]),
        ],
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        entry_points='''
            [console_scripts]
            sla-cli=sla_cli.entry:cli
        '''
    )
