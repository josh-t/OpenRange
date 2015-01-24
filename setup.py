"""rangetools installer"""

# -----------------------------------------------------------------------------

from codecs import open
from os import pardir, path
from setuptools import setup, find_packages
import rangetools

# -----------------------------------------------------------------------------

# path to this file's directory
PROJECT_ROOT = path.normpath(path.join(path.abspath(__file__), pardir))

with open(path.join(PROJECT_ROOT, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open(path.join(PROJECT_ROOT, 'VERSION')) as f:
    VERSION = f.read().strip()

# -----------------------------------------------------------------------------

setup(
    author="Josh Tomlinson",
    author_email="joshetomlinson@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Tools for expanded numerical range processing.",
    keywords="range ranges tools rangetool rangelist inclusive",
    license='MIT',
    long_description=LONG_DESCRIPTION,
    name='rangetools',
    packages=find_packages(),
    url="https://github.com/josh-t/rangetools",
    version=VERSION,
)

