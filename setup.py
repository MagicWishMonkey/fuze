import os
from setuptools import setup
from setuptools import find_packages

readme, dependencies = "", []
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

with open("readme.txt") as f:
    readme = f.read()


setup(
    name = "fuze",
    version = "1.0",
    author = "Ron!",
    author_email = "rodenberg@gmail.com",
    description = "A simple framework.",
    license = "MIT",
    #url = "http://packages.python.org/fuze",
    #package_dir = {"fuze": "fuze"},
    #packages=["fuze"],
    packages=find_packages(),
    long_description=readme,
    install_requires=dependencies
)