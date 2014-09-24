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
    description = "The fuze framework.",
    license = "MIT",
    #url = "http://packages.python.org/fuze",
    packages=find_packages("fuze"),
    long_description=readme,
    install_requires=dependencies
)