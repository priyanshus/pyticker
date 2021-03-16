from inspect import getsource
from os.path import abspath, dirname, join

from setuptools import setup, find_packages

here = abspath(dirname(getsource(lambda: 0)))

setup(
    name="pyticker",
    version="0.1-beta",
    description="Terminal based stocks and portfolio tracks.",
    long_description="Terminal based stocks watchlist and portfolio/position tracker.",
    url="https://github.com/priyanshus/pyticker",
    python_requires=">=3.8",
    license="MIT",
    install_requires=["prompt-toolkit>=3.0.3", "dataclasses-json>=0.5.2", "requests>=2.25.1"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="terminal-app finance stocks ticker",
    packages=find_packages(),
    entry_points={"console_scripts": ["pyticker = pyticker.pyticker_main:main"]}
)
