import setuptools
from dycow.settings import VERSION


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dycow",
    version=VERSION,
    scripts=['./scripts/dw', './scripts/dycow'],
    author="Sanix-darker",
    author_email="s4nixd@gmail.com",
    description="A tiny web-server app with a configuration file, NO NEED TO CODE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanix-darker/dycow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
