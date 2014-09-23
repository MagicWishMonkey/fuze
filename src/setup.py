import os
from setuptools import setup

readme, dependencies = "", []
with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

with open("readme.txt") as f:
    readme = f.read()


setup(
    name = "fuze",
    version = "0.0.1",
    author = "Ron!",
    author_email = "rodenberg@gmail.com",
    description = "A simple framework.",
    license = "MIT",
    url = "http://packages.python.org/wutwut",
    packages=["fuze"],
    long_description=readme,
    install_requires=dependencies
)