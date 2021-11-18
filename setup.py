#  ------------------------------------------
#   Copyright (c) Rygor. 2021.
#  ------------------------------------------

from setuptools import setup, find_packages

setup(
    name="kalc",
    version="0.6",
    license="MIT",
    description="Command Line Calculator",
    author="Rygor",
    author_email="pisemco@gmail.com",
    url="https://rygor.by",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["click", "pyperclip", "appdirs"],
    entry_points={
        "console_scripts": [
            "kalc = kalc.cli:kalc",
        ]
    },
)
