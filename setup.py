#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

from setuptools import setup, find_packages
from kalc import __version__

setup(
    name="kalc",
    version=__version__,
    license="MIT",
    description="Command Line Calculator",
    author="Rygor",
    author_email="pisemco@gmail.com",
    url="https://rygor.by",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["click", "pyperclip", "yapsy", "click_log"],
    entry_points={
        "console_scripts": [
            "kalc = kalc.cli:kalc",
        ]
    },
)
